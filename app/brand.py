"""Central access to the STEPS logo and app icon for the desktop app.

Every window, dialog and package takes its brand images from here. The files
are rendered from the masters in ``design/brand`` by
``scripts/build_brand_assets.py``.
"""

from __future__ import annotations

import functools
import re
import sys
from pathlib import Path

__all__ = [
    "APP_ICON_SIZES",
    "LOGO_SIZES",
    "MACOS_ICON_SHARE",
    "app_icon_ico_path",
    "app_icon_path",
    "apply_window_icon",
    "load_in_app_logo",
    "logo_path",
]

ASSETS = Path(__file__).resolve().parent / "assets/brand"
ICON_MASTER_SVG = Path(__file__).resolve().parents[1] / "design/brand/Logo_Steps-03.svg"
MACOS_ICON_SHARE = 824 / 1024  # Apple macOS 11+ icon squircle ratio with transparent margin.
LOGO_SIZES = (64, 128, 256)
APP_ICON_SIZES = (16, 32, 64, 256, 512)
WINDOW_ICON_SIZES = (256, 64, 32, 16)


def _stored_size(size: int, sizes: tuple[int, ...]) -> int:
    """Choose the smallest stored size that covers ``size``, else the largest."""
    return min((stored for stored in sizes if stored >= size), default=max(sizes))


def logo_path(size: int = 128) -> Path:
    """Return the transparent in-app logo that covers ``size`` pixels."""
    return ASSETS / f"steps-logo-{_stored_size(size, LOGO_SIZES)}.png"


def app_icon_path(size: int = 256) -> Path:
    """Return the app icon with its frame that covers ``size`` pixels."""
    return ASSETS / f"steps-app-icon-{_stored_size(size, APP_ICON_SIZES)}.png"


def app_icon_ico_path() -> Path:
    """Return the Windows icon file for executables and shortcuts."""
    return ASSETS / "steps.ico"


@functools.lru_cache(maxsize=1)
def _macos_svg_icon_data() -> str | None:
    """Render SVG app icon with macOS standard outer margin so Dock sizing matches native apps."""
    if not ICON_MASTER_SVG.is_file():
        return None
    svg = ICON_MASTER_SVG.read_text(encoding="utf-8")
    for cls, color in re.findall(r"\.([\w-]+)\s*\{\s*fill:\s*(#[0-9a-fA-F]{6})\s*;\s*\}", svg):
        svg = svg.replace(f'class="{cls}"', f'fill="{color}"')
    svg = re.sub(r"<defs>.*?</defs>", "", svg, flags=re.S)
    vb_match = re.search(r'viewBox="([^"]+)"', svg)
    vx, vy, vw, vh = (
        tuple(float(v) for v in vb_match.group(1).split()) if vb_match else (0.0, 0.0, 841.89, 841.89)
    )
    side = max(vw, vh)
    total = side / MACOS_ICON_SHARE
    ox = vx - (total - vw) / 2
    oy = vy - (total - vh) / 2
    svg = re.sub(r'width="[^"]*"', f'width="{total:.3f}"', svg, count=1)
    svg = re.sub(r'height="[^"]*"', f'height="{total:.3f}"', svg, count=1)
    svg = re.sub(r'viewBox="[^"]*"', f'viewBox="{ox:.3f} {oy:.3f} {total:.3f} {total:.3f}"', svg, count=1)
    return svg


def _load_macos_svg_icon_photos(root) -> list:
    from tkinter import PhotoImage, TclError

    svg_data = _macos_svg_icon_data()
    if not svg_data:
        return []
    photos = []
    for size in WINDOW_ICON_SIZES:
        try:
            rendered = PhotoImage(master=root, data=svg_data, format=f"svg -scaletowidth {size}")
        except TclError:
            return []
        if rendered.width() != size or rendered.height() != size:
            cropped = PhotoImage(master=root, width=size, height=size)
            cropped.tk.call(
                cropped.name,
                "copy",
                rendered.name,
                "-from",
                0,
                0,
                min(size, rendered.width()),
                min(size, rendered.height()),
            )
            rendered.tk.call("image", "delete", rendered.name)
            rendered = cropped
        photos.append(rendered)
    return photos


def apply_window_icon(root) -> None:
    """Give a Tk root window and the dialogs it opens later the STEPS app icon."""
    from tkinter import PhotoImage

    photos = _load_macos_svg_icon_photos(root) if sys.platform == "darwin" else []
    if not photos:
        photos = [PhotoImage(master=root, file=str(app_icon_path(size))) for size in WINDOW_ICON_SIZES]
    root.iconphoto(True, *photos)
    root._steps_icon_photos = photos  # Tk drops images that Python no longer references.


def load_in_app_logo(master, target_height: int = 28):
    """Load the transparent in-app STEPS logo scaled cleanly for the header."""
    from tkinter import PhotoImage

    photo = PhotoImage(master=master, file=str(logo_path(64)))
    if target_height <= 32 and photo.height() >= 64:
        photo = photo.subsample(2, 2)
    master._steps_logo_photo = photo
    return photo
