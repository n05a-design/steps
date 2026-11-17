"""
STEPS MIDI Core: Robust SMF Format 0 & Format 1 Parser & Format Conversion (OA-0028, M11).

Adheres to:
- MMA Standard MIDI File 1.0 Specification
- Format 0 (single track, multi-channel) and Format 1 (multi-track synchronous)
- Running status across channel voice messages
- Strict validation with MidiParseError on corrupt headers or truncated payloads
- Accurate Note-On / Note-Off event pairing into ParsedMidiNote records
- Lossless Format 1 <-> Format 0 conversion
- 100% pure Python standard library (struct, math)
"""

from __future__ import annotations

import math
import struct
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .smf import MidiFile, MidiTrack, RawMidiEvent
from .vlq import decode_vlq, encode_vlq


class MidiParseError(ValueError):
    """Raised when parsing corrupt or invalid SMF byte streams."""
    pass


@dataclass
class ParsedMidiEvent:
    """Represents a fully decoded MIDI event with absolute and delta tick positions."""
    abs_tick: int
    delta_ticks: int
    event_type: str  # 'note_on', 'note_off', 'poly_aftertouch', 'control_change', 'program_change', 'aftertouch', 'pitch_bend', 'sysex', 'meta'
    channel: Optional[int] = None
    data1: Optional[int] = None
    data2: Optional[int] = None
    meta_type: Optional[int] = None
    meta_data: Optional[bytes] = None
    raw_bytes: bytes = b""


@dataclass
class ParsedMidiNote:
    """Represents a paired musical note with explicit start tick and duration."""
    start_tick: int
    duration_ticks: int
    pitch: int
    velocity: int
    channel: int

    @property
    def end_tick(self) -> int:
        return self.start_tick + self.duration_ticks


@dataclass
class ParsedTrack:
    """Represents a parsed SMF track chunk."""
    track_index: int
    name: str = ""
    events: List[ParsedMidiEvent] = field(default_factory=list)
    notes: List[ParsedMidiNote] = field(default_factory=list)

    @property
    def total_ticks(self) -> int:
        if not self.events:
            return 0
        return self.events[-1].abs_tick


@dataclass
class ParsedSMF:
    """Represents a completely parsed Standard MIDI File."""
    format: int  # 0 or 1
    division: int  # ticks per quarter note
    tracks: List[ParsedTrack] = field(default_factory=list)

    @property
    def num_tracks(self) -> int:
        return len(self.tracks)

    @property
    def all_notes(self) -> List[ParsedMidiNote]:
        """Returns all notes across all tracks, sorted chronologically."""
        notes: List[ParsedMidiNote] = []
        for track in self.tracks:
            notes.extend(track.notes)
        return sorted(notes, key=lambda n: (n.start_tick, n.channel, n.pitch))

    @property
    def tempos(self) -> List[Tuple[int, float]]:
        """Returns list of (tick, bpm) tempo changes found in the file."""
        tempos: List[Tuple[int, float]] = []
        for track in self.tracks:
            for ev in track.events:
                if ev.event_type == "meta" and ev.meta_type == 0x51 and ev.meta_data and len(ev.meta_data) == 3:
                    us_per_quarter = struct.unpack(">I", b"\x00" + ev.meta_data)[0]
                    if us_per_quarter > 0:
                        bpm = round(60_000_000.0 / us_per_quarter, 3)
                        tempos.append((ev.abs_tick, bpm))
        return sorted(tempos, key=lambda t: t[0])

    @property
    def time_signatures(self) -> List[Tuple[int, int, int]]:
        """Returns list of (tick, numerator, denominator) time signatures."""
        ts: List[Tuple[int, int, int]] = []
        for track in self.tracks:
            for ev in track.events:
                if ev.event_type == "meta" and ev.meta_type == 0x58 and ev.meta_data and len(ev.meta_data) >= 2:
                    num = ev.meta_data[0]
                    denom = 2 ** ev.meta_data[1]
                    ts.append((ev.abs_tick, num, denom))
        return sorted(ts, key=lambda t: t[0])


class SMFParser:
    """High-integrity parser for Standard MIDI Files (Format 0 and Format 1)."""

    @classmethod
    def parse(cls, data: bytes) -> ParsedSMF:
        """
        Parses SMF byte stream, strictly validating chunk headers, running status,
        and pairing Note-On / Note-Off messages into musical notes.
        """
        if len(data) < 14:
            raise MidiParseError(f"MIDI file too short ({len(data)} bytes, min header is 14 bytes)")
        if data[:4] != b"MThd":
            raise MidiParseError(f"Invalid MIDI header magic: expected b'MThd', got {data[:4]!r}")

        header_len = struct.unpack(">I", data[4:8])[0]
        if header_len < 6:
            raise MidiParseError(f"Invalid MThd chunk length: {header_len} (must be >= 6)")

        smf_format, num_tracks, division = struct.unpack(">HHH", data[8:14])
        if smf_format not in (0, 1):
            raise MidiParseError(f"Unsupported SMF format {smf_format}. Only formats 0 and 1 are supported.")
        if division <= 0:
            raise MidiParseError(f"Invalid division: {division}. Must be positive ticks-per-quarter-note.")
        if division & 0x8000:
            raise MidiParseError("SMPTE division format is not supported.")

        if smf_format == 0 and num_tracks != 1:
            raise MidiParseError(f"SMF Format 0 must specify exactly 1 track, header specifies {num_tracks}")

        parsed_smf = ParsedSMF(format=smf_format, division=division)

        offset = 8 + header_len
        found_tracks = 0

        while offset < len(data):
            if offset + 8 > len(data):
                raise MidiParseError(f"Truncated chunk header at byte offset {offset}")

            chunk_magic = data[offset:offset + 4]
            chunk_len = struct.unpack(">I", data[offset + 4:offset + 8])[0]
            offset += 8

            if offset + chunk_len > len(data):
                raise MidiParseError(
                    f"Truncated chunk '{chunk_magic.decode('latin1', errors='replace')}' at offset {offset}: "
                    f"needs {chunk_len} bytes, only {len(data) - offset} remaining"
                )

            chunk_data = data[offset:offset + chunk_len]
            offset += chunk_len

            if chunk_magic == b"MTrk":
                parsed_track = cls._parse_track(found_tracks, chunk_data)
                parsed_smf.tracks.append(parsed_track)
                found_tracks += 1
            else:
                # Per SMF spec, unrecognized chunks should be ignored
                continue

        if found_tracks != num_tracks:
            raise MidiParseError(f"MThd specified {num_tracks} tracks, but parsed {found_tracks} MTrk chunks")

        return parsed_smf

    @classmethod
    def _parse_track(cls, track_index: int, data: bytes) -> ParsedTrack:
        """Parses a single MTrk byte payload into events and paired notes."""
        pos = 0
        current_tick = 0
        running_status: Optional[int] = None
        events: List[ParsedMidiEvent] = []
        track_name = ""

        # Open Note-Ons awaiting Note-Off: map (channel, pitch) -> list of (start_tick, velocity)
        open_notes: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
        paired_notes: List[ParsedMidiNote] = []

        while pos < len(data):
            delta, consumed = decode_vlq(data, pos)
            pos += consumed
            current_tick += delta

            if pos >= len(data):
                break

            status_byte = data[pos]

            if status_byte == 0xFF:
                # Meta Event: 0xFF <type> <length:vlq> <data>
                pos += 1
                if pos >= len(data):
                    raise MidiParseError(f"Unexpected EOF in meta event type at offset {pos}")
                meta_type = data[pos]
                pos += 1
                meta_len, consumed = decode_vlq(data, pos)
                pos += consumed
                if pos + meta_len > len(data):
                    raise MidiParseError(f"Truncated meta event data (type 0x{meta_type:02X}) at offset {pos}")
                meta_data = data[pos:pos + meta_len]
                pos += meta_len

                ev = ParsedMidiEvent(
                    abs_tick=current_tick,
                    delta_ticks=delta,
                    event_type="meta",
                    meta_type=meta_type,
                    meta_data=meta_data,
                    raw_bytes=b"\xFF" + bytes([meta_type]) + encode_vlq(meta_len) + meta_data,
                )
                events.append(ev)

                if meta_type == 0x03:  # Track Name
                    track_name = meta_data.decode("utf-8", errors="replace")
                elif meta_type == 0x2F:  # End of Track
                    running_status = None
                    break

                running_status = None

            elif status_byte in (0xF0, 0xF7):
                # System Exclusive event
                pos += 1
                sysex_len, consumed = decode_vlq(data, pos)
                pos += consumed
                if pos + sysex_len > len(data):
                    raise MidiParseError(f"Truncated Sysex event at offset {pos}")
                sysex_data = data[pos:pos + sysex_len]
                pos += sysex_len

                ev = ParsedMidiEvent(
                    abs_tick=current_tick,
                    delta_ticks=delta,
                    event_type="sysex",
                    raw_bytes=bytes([status_byte]) + encode_vlq(sysex_len) + sysex_data,
                )
                events.append(ev)
                running_status = None

            else:
                # Channel Voice or Mode message
                if status_byte & 0x80:
                    status = status_byte
                    pos += 1
                    running_status = status
                elif running_status is not None:
                    status = running_status
                else:
                    raise MidiParseError(f"Missing running status for byte 0x{status_byte:02X} at offset {pos}")

                msg_type = status & 0xF0
                channel = status & 0x0F

                if msg_type in (0x80, 0x90, 0xA0, 0xB0, 0xE0):
                    # 2-byte data messages
                    if pos + 2 > len(data):
                        raise MidiParseError(f"Truncated 2-byte channel message (status 0x{status:02X}) at offset {pos}")
                    d1 = data[pos]
                    d2 = data[pos + 1]
                    pos += 2
                    raw = struct.pack("BBB", status, d1, d2)

                    if msg_type == 0x80 or (msg_type == 0x90 and d2 == 0):
                        # Note Off
                        ev_name = "note_off"
                        cls._handle_note_off(channel, d1, current_tick, open_notes, paired_notes)
                    elif msg_type == 0x90:
                        # Note On
                        ev_name = "note_on"
                        cls._handle_note_on(channel, d1, d2, current_tick, open_notes)
                    elif msg_type == 0xA0:
                        ev_name = "poly_aftertouch"
                    elif msg_type == 0xB0:
                        ev_name = "control_change"
                    elif msg_type == 0xE0:
                        ev_name = "pitch_bend"
                    else:
                        ev_name = "channel_msg"

                    events.append(ParsedMidiEvent(
                        abs_tick=current_tick,
                        delta_ticks=delta,
                        event_type=ev_name,
                        channel=channel,
                        data1=d1,
                        data2=d2,
                        raw_bytes=raw,
                    ))

                elif msg_type in (0xC0, 0xD0):
                    # 1-byte data messages (Program Change, Channel Pressure)
                    if pos + 1 > len(data):
                        raise MidiParseError(f"Truncated 1-byte channel message (status 0x{status:02X}) at offset {pos}")
                    d1 = data[pos]
                    pos += 1
                    raw = struct.pack("BB", status, d1)

                    ev_name = "program_change" if msg_type == 0xC0 else "aftertouch"
                    events.append(ParsedMidiEvent(
                        abs_tick=current_tick,
                        delta_ticks=delta,
                        event_type=ev_name,
                        channel=channel,
                        data1=d1,
                        raw_bytes=raw,
                    ))
                else:
                    raise MidiParseError(f"Unsupported MIDI status byte 0x{status:02X} at offset {pos}")

        # Close any lingering open notes at track end
        for (ch, pitch), notes_list in open_notes.items():
            for start_tick, vel in notes_list:
                dur = max(1, current_tick - start_tick)
                paired_notes.append(ParsedMidiNote(
                    start_tick=start_tick,
                    duration_ticks=dur,
                    pitch=pitch,
                    velocity=vel,
                    channel=ch,
                ))

        paired_notes.sort(key=lambda n: (n.start_tick, n.channel, n.pitch))
        return ParsedTrack(
            track_index=track_index,
            name=track_name,
            events=events,
            notes=paired_notes,
        )

    @staticmethod
    def _handle_note_on(
        channel: int,
        pitch: int,
        velocity: int,
        tick: int,
        open_notes: Dict[Tuple[int, int], List[Tuple[int, int]]],
    ) -> None:
        key = (channel, pitch)
        if key not in open_notes:
            open_notes[key] = []
        open_notes[key].append((tick, velocity))

    @staticmethod
    def _handle_note_off(
        channel: int,
        pitch: int,
        tick: int,
        open_notes: Dict[Tuple[int, int], List[Tuple[int, int]]],
        paired_notes: List[ParsedMidiNote],
    ) -> None:
        key = (channel, pitch)
        if key in open_notes and open_notes[key]:
            # Pair with earliest Note-On (FIFO)
            start_tick, vel = open_notes[key].pop(0)
            dur = max(1, tick - start_tick)
            paired_notes.append(ParsedMidiNote(
                start_tick=start_tick,
                duration_ticks=dur,
                pitch=pitch,
                velocity=vel,
                channel=channel,
            ))


def convert_format_1_to_0(midi_file: MidiFile) -> MidiFile:
    """
    Converts a Format 1 multi-track MidiFile into a Format 0 single-track MidiFile.
    All events from all tracks are merged chronologically into track 0 while preserving
    channel numbers and meta-events.
    """
    if midi_file.format == 0:
        return midi_file

    out_file = MidiFile(smf_format=0, division=midi_file.division)
    single_track = out_file.add_track()

    all_raw: List[RawMidiEvent] = []
    for track in midi_file.tracks:
        all_raw.extend(track.raw_events)

    # Sort all raw events by tick (and note_off before note_on at same tick)
    all_raw.sort()
    single_track._raw_events = all_raw
    return out_file


def convert_format_0_to_1(midi_file: MidiFile) -> MidiFile:
    """
    Converts a Format 0 single-track MidiFile into a Format 1 multi-track MidiFile.
    Track 0 receives all global meta-events (tempo, time/key signature).
    Subsequent tracks are created per unique MIDI channel found in the stream.
    """
    if midi_file.format == 1:
        return midi_file

    out_file = MidiFile(smf_format=1, division=midi_file.division)
    meta_track = out_file.add_track()
    meta_track.name = "Tempo / Master"

    channel_tracks: Dict[int, MidiTrack] = {}

    src_track = midi_file.tracks[0] if midi_file.tracks else MidiTrack()
    for ev in src_track.raw_events:
        msg = ev.msg_bytes
        if not msg:
            continue

        first_byte = msg[0]
        if first_byte == 0xFF:
            # Meta event -> put in track 0
            meta_track._raw_events.append(ev)
        elif first_byte in (0xF0, 0xF7):
            # Sysex -> put in track 0
            meta_track._raw_events.append(ev)
        else:
            channel = first_byte & 0x0F
            if channel not in channel_tracks:
                t = out_file.add_track()
                t.name = f"Channel {channel + 1}"
                channel_tracks[channel] = t
            channel_tracks[channel]._raw_events.append(ev)

    return out_file


__all__ = [
    "MidiParseError",
    "ParsedMidiEvent",
    "ParsedMidiNote",
    "ParsedTrack",
    "ParsedSMF",
    "SMFParser",
    "convert_format_1_to_0",
    "convert_format_0_to_1",
]
