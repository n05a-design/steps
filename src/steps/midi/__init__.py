"""STEPS MIDI subsystem: SMF Format 0 & 1 generation, parsing, time engine, and export service."""
from __future__ import annotations

from .export_service import MidiExportService
from .smf import MidiFile, MidiTrack, RawMidiEvent
from .smf_parser import (
    MidiParseError,
    ParsedMidiEvent,
    ParsedMidiNote,
    ParsedSMF,
    ParsedTrack,
    SMFParser,
    convert_format_0_to_1,
    convert_format_1_to_0,
)
from .time import BarBeatPosition, RationalMidiTime
from .vlq import decode_vlq, encode_vlq

__all__ = [
    # VLQ
    "encode_vlq",
    "decode_vlq",
    # SMF generator
    "RawMidiEvent",
    "MidiTrack",
    "MidiFile",
    "MidiExportService",
    # SMF parser & converter (OA-0028)
    "MidiParseError",
    "ParsedMidiEvent",
    "ParsedMidiNote",
    "ParsedTrack",
    "ParsedSMF",
    "SMFParser",
    "convert_format_1_to_0",
    "convert_format_0_to_1",
    # Rational time engine (OA-0029)
    "BarBeatPosition",
    "RationalMidiTime",
]
