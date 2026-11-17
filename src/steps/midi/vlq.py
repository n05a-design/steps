"""
STEPS MIDI Core: Variable-Length Quantity (VLQ) Encoding and Decoding.

Adheres to Standard MIDI Files 1.0 Specification.
In VLQ, values are represented as a sequence of 7-bit values, most significant first.
The most significant bit (bit 7) of all bytes is set to 1, except for the last byte
which has bit 7 clear (0).
"""

from __future__ import annotations


def encode_vlq(value: int) -> bytes:
    """Encodes an integer >= 0 into standard MIDI variable-length quantity bytes."""
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"VLQ value must be non-negative integer, got {value}")
    if value == 0:
        return b"\x00"

    buffer = bytearray()
    buffer.append(value & 0x7F)
    value >>= 7

    while value > 0:
        buffer.append((value & 0x7F) | 0x80)
        value >>= 7

    buffer.reverse()
    return bytes(buffer)


def decode_vlq(data: bytes, offset: int = 0) -> tuple[int, int]:
    """
    Decodes a variable-length quantity from data starting at offset.
    Returns (value, bytes_consumed).
    """
    if offset >= len(data):
        raise ValueError("Unexpected end of data while decoding VLQ")

    value = 0
    consumed = 0

    while True:
        if offset + consumed >= len(data):
            raise ValueError("Truncated VLQ sequence")
        b = data[offset + consumed]
        consumed += 1
        value = (value << 7) | (b & 0x7F)
        if not (b & 0x80):
            break
        if consumed > 4:
            raise ValueError("VLQ value exceeds 4 bytes (invalid SMF delta-time)")

    return value, consumed
