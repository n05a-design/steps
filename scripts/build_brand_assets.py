"""Render the STEPS logo masters into the app's PNG and ICO assets.

The SVG masters in ``design/brand`` are the only source. This script rasterises
them with the standard library, so the outputs can be rebuilt and checked on
every platform of the CI matrix without an image dependency.

``--check`` compares decoded pixels instead of file bytes, because zlib builds
may compress the same pixels differently.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import groupby
from pathlib import Path
import re
import struct
import sys
import xml.etree.ElementTree as ET
import zlib

ROOT = Path(__file__).resolve().parents[1]
MASTERS = ROOT / "design/brand"
OUTPUT = ROOT / "app/assets/brand"

# Byte identity with the owner's graphic master (see design/brand/README.md).
MASTER_SHA256 = {
    "Logo_Steps-01.svg": "52d8dd13bf891e8fda193331b515410ef21c4c4158b13e2714b868b5401ff8a5",
    "Logo_Steps-02.svg": "7c055db3ed30897bfa735b4679ddf8542758bc4a5d59af1ae75057496f8b8304",
    "Logo_Steps-03.svg": "3ef4e5b10dda816add78bfc404a6fb9e95651136c5dea0522a192cacc039efa9",
}
LOGO_MASTER = "Logo_Steps-01.svg"
ICON_MASTER = "Logo_Steps-03.svg"
LOGO_SIZES = (64, 128, 256)
ICON_SIZES = (16, 32, 64, 256, 512)
ICO_SIZES = (16, 24, 32, 48, 64, 128, 256)
ICO_BITMAP_LIMIT = 48  # Larger entries are stored as PNG, as Windows expects for 256 px.
LOGO_PADDING = 0.02  # Share of the mark's longer side kept free around the in-app logo.
SUBSAMPLES = 8

_TOKEN = re.compile(r"[A-Za-z]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")
_FILL = re.compile(r"\.([\w-]+)\s*\{[^}]*?fill:\s*#([0-9a-fA-F]{6})")
_ARITY = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "Z": 0}


def _curve(points, p0, p1, p2, p3):
    """Append a cubic Bezier as line points; the step count follows its length."""
    length = sum(
        ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        for a, b in ((p0, p1), (p1, p2), (p2, p3))
    )
    steps = min(96, max(8, int(length / 4) + 1))
    for index in range(1, steps + 1):
        t = index / steps
        u = 1 - t
        a, b, c, d = u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t
        points.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
                       a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))


def parse_path(data):
    """Return the closed subpaths of an SVG path as point lists in user units."""
    tokens = _TOKEN.findall(data)
    subpaths, points = [], []
    x = y = start_x = start_y = 0.0
    control = None  # Last control point as (kind, x, y) for the smooth commands.
    position, command = 0, None
    while position < len(tokens):
        if tokens[position].isalpha():
            command = tokens[position]
            position += 1
        elif command is None:
            raise ValueError("Path data starts without a command.")
        kind = command.upper()
        if kind not in _ARITY:
            raise ValueError(f"Unsupported path command {command!r}.")
        try:
            values = [float(token) for token in tokens[position:position + _ARITY[kind]]]
        except ValueError as exc:
            raise ValueError(f"Incomplete arguments for path command {command!r}.") from exc
        if len(values) != _ARITY[kind]:
            raise ValueError(f"Incomplete arguments for path command {command!r}.")
        position += _ARITY[kind]
        relative = command.islower()
        if relative and kind == "H":
            values[0] += x
        elif relative and kind == "V":
            values[0] += y
        elif relative:
            values = [value + (x if index % 2 == 0 else y) for index, value in enumerate(values)]
        reflected = None
        if kind == "M":
            if len(points) > 1:
                subpaths.append(points)
            x, y = start_x, start_y = values
            points = [(x, y)]
            command = "l" if relative else "L"  # Further pairs are implicit line-tos.
        elif kind == "Z":
            if len(points) > 1:
                subpaths.append(points)
            x, y = start_x, start_y
            points = [(x, y)]
            command = None  # Closing takes no numbers; the next token must be a command.
        elif kind == "L":
            x, y = values
            points.append((x, y))
        elif kind == "H":
            x = values[0]
            points.append((x, y))
        elif kind == "V":
            y = values[0]
            points.append((x, y))
        elif kind in "CS":
            if kind == "S":
                first = (2 * x - control[1], 2 * y - control[2]) if control and control[0] == "C" else (x, y)
                values = [*first, *values]
            _curve(points, (x, y), values[0:2], values[2:4], values[4:6])
            reflected = ("C", values[2], values[3])
            x, y = values[4:6]
        else:  # Q and T: raise the quadratic curve to a cubic one.
            if kind == "T":
                first = (2 * x - control[1], 2 * y - control[2]) if control and control[0] == "Q" else (x, y)
                values = [*first, *values]
            qx, qy, end_x, end_y = values
            _curve(points, (x, y),
                   (x + 2 / 3 * (qx - x), y + 2 / 3 * (qy - y)),
                   (end_x + 2 / 3 * (qx - end_x), end_y + 2 / 3 * (qy - end_y)),
                   (end_x, end_y))
            reflected = ("Q", qx, qy)
            x, y = end_x, end_y
        control = reflected
    if len(points) > 1:
        subpaths.append(points)
    return subpaths


def load_master(name):
    """Read one master as painting order of ``(rgb, subpaths)`` after checking its hash."""
    content = (MASTERS / name).read_bytes()
    if sha256(content).hexdigest() != MASTER_SHA256[name]:
        raise ValueError(f"{name} differs from the registered master (SHA-256).")
    root = ET.fromstring(content)
    fills = {}
    shapes = []
    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1]
        if "transform" in element.attrib:
            raise ValueError(f"{name}: transforms are outside this renderer.")
        if tag == "style":
            for class_name, colour in _FILL.findall(element.text or ""):
                fills[class_name] = tuple(int(colour[index:index + 2], 16) for index in (0, 2, 4))
        elif tag == "path":
            shapes.append((fills[element.attrib["class"]], parse_path(element.attrib["d"])))
        elif tag not in {"svg", "defs", "g"}:
            raise ValueError(f"{name}: element <{tag}> is outside this renderer.")
    return shapes


def bounds(shapes):
    """Return ``(left, top, right, bottom)`` of all shapes in user units."""
    xs = [point[0] for _, subpaths in shapes for path in subpaths for point in path]
    ys = [point[1] for _, subpaths in shapes for path in subpaths for point in path]
    return min(xs), min(ys), max(xs), max(ys)


def square_frame(box, padding=0.0):
    """Return origin and edge of the centred square that contains ``box``."""
    left, top, right, bottom = box
    edge = max(right - left, bottom - top) * (1 + 2 * padding)
    return (left + right - edge) / 2, (top + bottom - edge) / 2, edge


def _coverage(subpaths, size, origin_x, origin_y, scale):
    """Return ``{row: coverage list}`` of a non-zero filled shape in pixel space."""
    crossings = {}
    for path in subpaths:
        pixels = [((px - origin_x) * scale, (py - origin_y) * scale) for px, py in path]
        for (x0, y0), (x1, y1) in zip(pixels, pixels[1:] + pixels[:1]):
            if y0 == y1:
                continue
            direction = 1 if y1 > y0 else -1
            if direction < 0:
                x0, y0, x1, y1 = x1, y1, x0, y0
            slope = (x1 - x0) / (y1 - y0)
            # Sample rows lie at (k + 0.5) / SUBSAMPLES and count for y0 <= row < y1.
            first = max(0, -int(-(y0 * SUBSAMPLES - 0.5) // 1))
            last = min(size * SUBSAMPLES - 1, -int(-(y1 * SUBSAMPLES - 0.5) // 1) - 1)
            for sample in range(first, last + 1):
                sample_y = (sample + 0.5) / SUBSAMPLES
                crossings.setdefault(sample, []).append((x0 + (sample_y - y0) * slope, direction))
    weight = 1 / SUBSAMPLES
    partial, steps = {}, {}
    for sample, hits in crossings.items():
        row = sample // SUBSAMPLES
        area = partial.setdefault(row, [0.0] * size)
        step = steps.setdefault(row, [0.0] * (size + 1))
        hits.sort()
        winding, span_start = 0, 0.0
        for hit_x, direction in hits:
            if winding == 0:
                span_start = hit_x
            winding += direction
            if winding:
                continue
            left, right = max(span_start, 0.0), min(hit_x, float(size))
            if right <= left:
                continue
            first_pixel, last_pixel = int(left), int(right)
            if first_pixel == last_pixel:
                area[first_pixel] += (right - left) * weight
                continue
            area[first_pixel] += (first_pixel + 1 - left) * weight
            if last_pixel < size:
                area[last_pixel] += (right - last_pixel) * weight
            step[first_pixel + 1] += weight
            step[last_pixel] -= weight
    rows = {}
    for row, area in partial.items():
        running, values = 0.0, []
        for column in range(size):
            running += steps[row][column]
            values.append(min(1.0, area[column] + running))
        rows[row] = values
    return rows


def render(shapes, size, frame):
    """Paint the shapes into ``size`` x ``size`` straight-alpha RGBA rows."""
    origin_x, origin_y, edge = frame
    scale = size / edge
    # Premultiplied colour per pixel as [red, green, blue, alpha] in 0..1.
    canvas = [[[0.0, 0.0, 0.0, 0.0] for _ in range(size)] for _ in range(size)]
    # Neighbouring shapes of one colour are painted as one area. Painted one by
    # one, their antialiased shared edges would let the background shine through.
    for (red, green, blue), run in groupby(shapes, key=lambda shape: shape[0]):
        source = (red / 255, green / 255, blue / 255)
        merged = {}
        for _, subpaths in run:
            for row, values in _coverage(subpaths, size, origin_x, origin_y, scale).items():
                known = merged.get(row)
                merged[row] = values if known is None else [
                    min(1.0, first + second) for first, second in zip(known, values)]
        for row, values in merged.items():
            line = canvas[row]
            for column, alpha in enumerate(values):
                if alpha <= 0.0:
                    continue
                pixel = line[column]
                keep = 1 - alpha
                pixel[0] = source[0] * alpha + pixel[0] * keep
                pixel[1] = source[1] * alpha + pixel[1] * keep
                pixel[2] = source[2] * alpha + pixel[2] * keep
                pixel[3] = alpha + pixel[3] * keep
    rows = []
    for line in canvas:
        row = bytearray()
        for red, green, blue, alpha in line:
            if alpha <= 0.0:
                row += b"\0\0\0\0"
                continue
            row += bytes((min(255, int(red / alpha * 255 + 0.5)),
                          min(255, int(green / alpha * 255 + 0.5)),
                          min(255, int(blue / alpha * 255 + 0.5)),
                          min(255, int(alpha * 255 + 0.5))))
        rows.append(bytes(row))
    return rows


def _chunk(kind, payload):
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload))


def encode_png(rows):
    """Encode straight-alpha RGBA rows as an 8-bit PNG without row filters."""
    size = len(rows)
    header = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    pixels = zlib.compress(b"".join(b"\0" + row for row in rows), 9)
    return b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", header) + _chunk(b"IDAT", pixels) + _chunk(b"IEND", b"")


def decode_png(content):
    """Return the RGBA rows of a PNG written by :func:`encode_png`."""
    if content[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a PNG file.")
    position, header, pixels = 8, None, b""
    while position < len(content):
        length, kind = struct.unpack(">I4s", content[position:position + 8])
        payload = content[position + 8:position + 8 + length]
        if kind == b"IHDR":
            header = struct.unpack(">IIBBBBB", payload)
        elif kind == b"IDAT":
            pixels += payload
        position += length + 12
    if header is None or header[0] != header[1] or header[2:] != (8, 6, 0, 0, 0):
        raise ValueError("Unexpected PNG layout.")
    size = header[0]
    raw = zlib.decompress(pixels)
    stride = size * 4 + 1
    if len(raw) != size * stride or any(raw[row * stride] for row in range(size)):
        raise ValueError("Unexpected PNG pixel data.")
    return [raw[row * stride + 1:(row + 1) * stride] for row in range(size)]


def _ico_bitmap(rows):
    """Encode RGBA rows as a 32-bit icon bitmap with its transparency mask."""
    size = len(rows)
    header = struct.pack("<IiiHHIIiiII", 40, size, size * 2, 1, 32, 0, 0, 0, 0, 0, 0)
    colour = bytearray()
    mask = bytearray()
    mask_stride = (size + 31) // 32 * 4
    for row in reversed(rows):
        bits = bytearray(mask_stride)
        for column in range(size):
            red, green, blue, alpha = row[column * 4:column * 4 + 4]
            colour += bytes((blue, green, red, alpha))
            if alpha == 0:
                bits[column // 8] |= 0x80 >> column % 8
        mask += bits
    return header + bytes(colour) + bytes(mask)


def encode_ico(images):
    """Pack ``{size: rgba rows}`` into one Windows icon file."""
    entries = []
    for size in sorted(images):
        rows = images[size]
        entries.append((size, _ico_bitmap(rows) if size <= ICO_BITMAP_LIMIT else encode_png(rows)))
    directory = struct.pack("<HHH", 0, 1, len(entries))
    offset = 6 + 16 * len(entries)
    body = b""
    for size, payload in entries:
        directory += struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(payload), offset)
        offset += len(payload)
        body += payload
    return directory + body


def decode_ico(content):
    """Return ``{size: rgba rows}`` of an icon written by :func:`encode_ico`."""
    _, kind, count = struct.unpack("<HHH", content[:6])
    if kind != 1:
        raise ValueError("Not an icon file.")
    images = {}
    for index in range(count):
        width, _, _, _, _, bits, length, offset = struct.unpack("<BBBBHHII", content[6 + 16 * index:22 + 16 * index])
        size = width or 256
        payload = content[offset:offset + length]
        if payload[:8] == b"\x89PNG\r\n\x1a\n":
            images[size] = decode_png(payload)
            continue
        if bits != 32 or struct.unpack("<IiiHH", payload[:16]) != (40, size, size * 2, 1, 32):
            raise ValueError("Unexpected icon bitmap layout.")
        rows = []
        for row in range(size - 1, -1, -1):
            line = payload[40 + row * size * 4:40 + (row + 1) * size * 4]
            rows.append(bytes(value for column in range(size)
                              for value in (line[column * 4 + 2], line[column * 4 + 1],
                                            line[column * 4], line[column * 4 + 3])))
        images[size] = rows
    return images


def build():
    """Render every output as ``{file name: (pixel content, file bytes)}``."""
    logo = load_master(LOGO_MASTER)
    logo_frame = square_frame(bounds(logo), LOGO_PADDING)
    icon = load_master(ICON_MASTER)
    icon_frame = square_frame(bounds(icon))
    icons = {size: render(icon, size, icon_frame) for size in sorted({*ICON_SIZES, *ICO_SIZES})}
    outputs = {}
    for size in LOGO_SIZES:
        rows = render(logo, size, logo_frame)
        outputs[f"steps-logo-{size}.png"] = (rows, encode_png(rows))
    for size in ICON_SIZES:
        outputs[f"steps-app-icon-{size}.png"] = (icons[size], encode_png(icons[size]))
    ico = {size: icons[size] for size in ICO_SIZES}
    outputs["steps.ico"] = (ico, encode_ico(ico))
    return outputs


def differences(outputs):
    """List outputs whose stored pixels differ from the freshly rendered ones."""
    problems = [f"unexpected file: {path.name}" for path in sorted(OUTPUT.iterdir())
                if path.name not in outputs] if OUTPUT.is_dir() else []
    for name, (pixels, _) in outputs.items():
        path = OUTPUT / name
        if not path.is_file():
            problems.append(f"missing: {name}")
            continue
        try:
            stored = (decode_ico if name.endswith(".ico") else decode_png)(path.read_bytes())
        except (ValueError, struct.error, zlib.error) as exc:
            problems.append(f"unreadable: {name} ({exc})")
            continue
        if stored != pixels:
            problems.append(f"outdated: {name}")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="compare the stored assets with the masters without writing")
    args = parser.parse_args()
    try:
        outputs = build()
    except (OSError, ValueError, KeyError, ET.ParseError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2
    if args.check:
        problems = differences(outputs)
        for problem in problems:
            print(problem, file=sys.stderr)
        if not problems:
            print(f"OK: {len(outputs)} brand assets match the masters.")
        return int(bool(problems))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for name, (_, content) in outputs.items():
        (OUTPUT / name).write_bytes(content)
        print(f"{name}: {len(content)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
