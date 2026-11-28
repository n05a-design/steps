"""
STEPS MIDI Core: Standard MIDI File (SMF) 1.0 Generator & Parser.

Adheres to:
- Standard MIDI File 1.0 Specification (Format 0 and Format 1)
- Strict delta-time calculation and terminal End-of-Track meta events
- 100% pure Python standard library (struct, math) without external C-extensions
"""

from __future__ import annotations

import errno
import math
import os
import stat
import struct
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional, Tuple

from .vlq import decode_vlq, encode_vlq


@dataclass
class RawMidiEvent:
    """Internal event with absolute tick timing, sorted before delta-time serialization."""
    abs_tick: int
    msg_bytes: bytes
    # Sort order key: abs_tick first, then note_off before note_on at same tick
    is_note_off: bool = False

    def __lt__(self, other: RawMidiEvent) -> bool:
        if self.abs_tick != other.abs_tick:
            return self.abs_tick < other.abs_tick
        if self.is_note_off != other.is_note_off:
            return self.is_note_off  # True (note_off) comes before False (note_on)
        return False


class MidiTrack:
    """Represents a single MIDI track containing musical and meta events."""

    def __init__(self, name: str = ""):
        self.name = name
        self._raw_events: List[RawMidiEvent] = []
        self._imported = False
        self._end_tick = 0
        if name:
            self.add_track_name(name)

    @property
    def raw_events(self) -> List[RawMidiEvent]:
        """Returns shallow copy of raw events recorded in this track."""
        return list(self._raw_events)

    def add_track_name(self, name: str) -> None:
        """Adds meta event 0x03 Track Name at tick 0."""
        text_bytes = name.encode("utf-8")
        payload = b"\xFF\x03" + encode_vlq(len(text_bytes)) + text_bytes
        self._raw_events.append(RawMidiEvent(abs_tick=0, msg_bytes=payload))

    def add_tempo(self, start_tick: int, bpm: float) -> None:
        """Adds meta event 0x51 Set Tempo."""
        if not math.isfinite(bpm) or bpm <= 0:
            raise ValueError(f"BPM must be finite and positive, got {bpm}")
        period = 60_000_000.0 / bpm
        if not math.isfinite(period) or not 1 <= round(period) <= 0xFFFFFF:
            raise ValueError(f"BPM cannot be represented as an SMF tempo, got {bpm}")
        us_bytes = round(period).to_bytes(3, "big")
        payload = b"\xFF\x51\x03" + us_bytes
        self._raw_events.append(RawMidiEvent(abs_tick=start_tick, msg_bytes=payload))

    def add_time_signature(self, start_tick: int, numerator: int = 4, denominator: int = 4) -> None:
        """Adds meta event 0x58 Time Signature."""
        denom_pow2 = int(math.log2(denominator)) if denominator in (1, 2, 4, 8, 16, 32) else 2
        # payload: numerator, denom_pow2, clocks_per_click (24), 32nd_notes_per_quarter (8)
        payload = b"\xFF\x58\x04" + struct.pack("BBBB", numerator, denom_pow2, 24, 8)
        self._raw_events.append(RawMidiEvent(abs_tick=start_tick, msg_bytes=payload))

    def add_key_signature(self, start_tick: int, accidentals: int = 0, is_minor: bool = False) -> None:
        """Adds meta event 0x59 Key Signature (accidentals: -7..+7, is_minor: bool)."""
        if not (-7 <= accidentals <= 7):
            raise ValueError(f"Key signature accidentals must be in [-7..7], got {accidentals}")
        mi = 1 if is_minor else 0
        payload = b"\xFF\x59\x02" + struct.pack("bb", accidentals, mi)
        self._raw_events.append(RawMidiEvent(abs_tick=start_tick, msg_bytes=payload))

    def add_note(
        self,
        start_tick: int,
        duration_ticks: int,
        pitch: int,
        velocity: int = 64,
        channel: int = 0
    ) -> None:
        """
        Adds a Note On event at start_tick and Note Off event at start_tick + duration_ticks.
        """
        if not (0 <= pitch <= 127):
            raise ValueError(f"MIDI pitch must be in 0..127, got {pitch}")
        if not (0 <= velocity <= 127):
            raise ValueError(f"MIDI velocity must be in 0..127, got {velocity}")
        if not (0 <= channel <= 15):
            raise ValueError(f"MIDI channel must be in 0..15, got {channel}")
        if duration_ticks <= 0:
            raise ValueError(f"duration_ticks must be > 0, got {duration_ticks}")

        status_on = 0x90 | (channel & 0x0F)
        status_off = 0x80 | (channel & 0x0F)

        # Note On
        msg_on = struct.pack("BBB", status_on, pitch, velocity)
        self._raw_events.append(RawMidiEvent(abs_tick=start_tick, msg_bytes=msg_on, is_note_off=False))

        # Note Off
        msg_off = struct.pack("BBB", status_off, pitch, 0)
        self._raw_events.append(RawMidiEvent(abs_tick=start_tick + duration_ticks, msg_bytes=msg_off, is_note_off=True))

    def _chronological_events(self) -> list[RawMidiEvent]:
        if self._imported:
            return sorted(self._raw_events, key=lambda event: event.abs_tick)
        return sorted(self._raw_events)

    def to_bytes(self) -> bytes:
        """
        Serializes this track into an SMF MTrk chunk with delta-time encoded events
        and a mandatory terminal End of Track event (00 FF 2F 00).
        """
        stream = bytearray()
        last_tick = 0

        for ev in self._chronological_events():
            delta = ev.abs_tick - last_tick
            if delta < 0:
                delta = 0
            stream.extend(encode_vlq(delta))
            stream.extend(ev.msg_bytes)
            last_tick = ev.abs_tick

        stream.extend(encode_vlq(max(0, self._end_tick - last_tick)))
        stream.extend(b"\xFF\x2F\x00")

        # Wrap in MTrk header
        length_bytes = struct.pack(">I", len(stream))
        return b"MTrk" + length_bytes + bytes(stream)


class MidiFile:
    """Represents a complete Standard MIDI File (SMF)."""

    def __init__(self, smf_format: int = 1, division: int = 480):
        if smf_format not in (0, 1):
            raise ValueError(f"Supported SMF formats are 0 and 1, got {smf_format}")
        if division <= 0 or division >= 0x8000:
            raise ValueError(f"Division must be a positive ticks-per-quarter-note <= 32767, got {division}")

        self.format = smf_format
        self.division = division
        self.tracks: List[MidiTrack] = []

    def add_track(self, track: Optional[MidiTrack] = None) -> MidiTrack:
        """Appends a new track to the file."""
        if self.format == 0 and len(self.tracks) >= 1:
            raise ValueError("SMF Format 0 can only contain exactly one track.")
        t = track if track is not None else MidiTrack()
        self.tracks.append(t)
        return t

    def to_bytes(self) -> bytes:
        """Serializes the complete SMF file into bytes."""
        if not self.tracks:
            # Guarantee at least one track
            self.add_track()

        num_tracks = len(self.tracks)
        # MThd header: length=6, format, num_tracks, division
        header = b"MThd" + struct.pack(">IHHH", 6, self.format, num_tracks, self.division)
        tracks_data = b"".join(t.to_bytes() for t in self.tracks)
        return header + tracks_data

    def save(self, file_path: Path | str) -> Path:
        """Writes the MIDI file to disk atomically."""
        data = self.to_bytes()
        path = Path(file_path)
        try:
            target = path.resolve()
        except RuntimeError as exc:
            error_code = getattr(errno, "ELOOP", errno.EINVAL)
            raise OSError(error_code, os.strerror(error_code), path) from exc
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            existing = target.stat()
        except FileNotFoundError:
            existing = None
        if existing is not None:
            if stat.S_ISDIR(existing.st_mode):
                raise IsADirectoryError(errno.EISDIR, os.strerror(errno.EISDIR), target)
            if not stat.S_ISREG(existing.st_mode):
                raise OSError(errno.EINVAL, "MIDI export requires a regular file", target)
            if not os.access(target, os.W_OK):
                raise PermissionError(errno.EACCES, os.strerror(errno.EACCES), target)

        with tempfile.TemporaryDirectory(
            prefix=".steps-midi-", dir=target.parent, ignore_cleanup_errors=True,
        ) as staging:
            pending = Path(staging) / "export.mid"
            with pending.open("xb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            if existing is not None:
                pending.chmod(stat.S_IMODE(existing.st_mode))
            os.replace(pending, target)
        return path

    @classmethod
    def from_bytes(cls, data: bytes) -> MidiFile:
        """
        Parses SMF bytes and verifies header structure and track chunks.
        """
        if len(data) < 14 or data[:4] != b"MThd":
            raise ValueError("Invalid SMF header: missing MThd magic")

        header_len = struct.unpack(">I", data[4:8])[0]
        if header_len < 6 or header_len > len(data) - 8:
            raise ValueError(f"Invalid MThd header length: {header_len}")

        smf_format, num_tracks, division = struct.unpack(">HHH", data[8:14])
        if smf_format not in (0, 1):
            raise ValueError(f"Unsupported SMF format: {smf_format}")
        if division & 0x8000:
            raise ValueError("SMPTE division not supported in pure SMF parser")

        if smf_format == 0 and num_tracks != 1:
            raise ValueError("SMF Format 0 must declare exactly one track.")
        midi = cls(smf_format=smf_format, division=division)

        offset = 8 + header_len
        found_tracks = 0

        while offset < len(data):
            if offset + 8 > len(data):
                raise ValueError("Truncated chunk header")
            chunk_type = data[offset:offset + 4]
            chunk_len = struct.unpack(">I", data[offset + 4:offset + 8])[0]
            offset += 8

            if offset + chunk_len > len(data):
                raise ValueError("Truncated chunk payload")

            if chunk_type == b"MTrk":
                found_tracks += 1
                # Parse track payload
                track = midi.add_track()
                track_data = data[offset:offset + chunk_len]
                _parse_track_events(track, track_data)

            offset += chunk_len

        if found_tracks != num_tracks:
            raise ValueError(f"Expected {num_tracks} tracks, found {found_tracks}")

        return midi


def _parse_track_events(track: MidiTrack, data: bytes) -> None:
    """Parses events from a single track chunk payload."""
    track._imported = True
    pos = 0
    current_tick = 0
    running_status: Optional[int] = None

    while pos < len(data):
        delta, consumed = decode_vlq(data, pos)
        pos += consumed
        current_tick += delta

        if pos >= len(data):
            raise ValueError("Missing event after delta.")

        status_byte = data[pos]

        if status_byte == 0xFF:
            if pos + 1 >= len(data):
                raise ValueError("Missing meta event type.")
            start = pos
            meta_type = data[pos + 1]
            meta_len, consumed = decode_vlq(data, pos + 2)
            payload = pos + 2 + consumed
            pos = payload + meta_len
            if pos > len(data):
                raise ValueError("Truncated meta event data.")
            if meta_type == 0x2F:
                if meta_len != 0 or pos != len(data):
                    raise ValueError("End of Track must have an empty payload and be the final event.")
                track._end_tick = current_tick
                break
            meta_data = data[payload:pos]
            if meta_type == 0x03:
                track.name = meta_data.decode("utf-8", errors="replace")
            elif meta_type == 0x51:
                _validate_set_tempo(meta_data)
            track._raw_events.append(RawMidiEvent(current_tick, data[start:pos]))
            running_status = None

        elif status_byte in (0xF0, 0xF7):
            start = pos
            sysex_len, consumed = decode_vlq(data, pos + 1)
            pos += 1 + consumed + sysex_len
            if pos > len(data):
                raise ValueError("Truncated SysEx event data.")
            track._raw_events.append(RawMidiEvent(current_tick, data[start:pos]))
            running_status = None

        else:
            # Channel voice message
            if status_byte & 0x80:
                status = status_byte
                pos += 1
                running_status = status
            elif running_status is not None:
                status = running_status
            else:
                raise ValueError(f"Invalid running status at pos {pos}")

            msg_type = status & 0xF0

            if msg_type in (0x80, 0x90, 0xA0, 0xB0, 0xE0):
                if pos + 2 > len(data):
                    raise ValueError("Truncated channel event data.")
                d1, d2 = data[pos:pos + 2]
                if (d1 | d2) & 0x80:
                    raise ValueError("Invalid channel data byte.")
                pos += 2
                is_note_off = (msg_type == 0x80) or (msg_type == 0x90 and d2 == 0)
                msg_bytes = struct.pack("BBB", status, d1, d2)
                track._raw_events.append(RawMidiEvent(abs_tick=current_tick, msg_bytes=msg_bytes, is_note_off=is_note_off))
            elif msg_type in (0xC0, 0xD0):
                if pos >= len(data):
                    raise ValueError("Truncated channel event data.")
                d1 = data[pos]
                if d1 & 0x80:
                    raise ValueError("Invalid channel data byte.")
                pos += 1
                msg_bytes = struct.pack("BB", status, d1)
                track._raw_events.append(RawMidiEvent(abs_tick=current_tick, msg_bytes=msg_bytes))
            else:
                raise ValueError(f"Unsupported MIDI status byte 0x{status:02X}.")


def _validate_set_tempo(data: bytes) -> None:
    if len(data) != 3 or not any(data):
        raise ValueError("Set Tempo requires three bytes and a positive period.")
