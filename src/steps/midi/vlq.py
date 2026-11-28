"""
STEPS MIDI Core: Variable-Length Quantity (VLQ) Encoding and Decoding.

Adheres to Standard MIDI Files 1.0 Specification.
In VLQ, values are represented as a sequence of 7-bit values, most significant first.
The most significant bit (bit 7) of all bytes is set to 1, except for the last byte
which has bit 7 clear (0).
"""

from __future__ import annotations

MAX_VLQ_VALUE = 0x0FFFFFFF


def encode_vlq(value: int) -> bytes:
    """Encode an SMF value representable in one to four VLQ bytes."""
    if type(value) is not int or not 0 <= value <= MAX_VLQ_VALUE:
        raise ValueError(f"VLQ value must be an integer in 0..{MAX_VLQ_VALUE}, got {value}")
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
    if type(offset) is not int or not 0 <= offset < len(data):
        raise ValueError("VLQ offset must identify a byte in the input")

    value = 0
    for pos in range(offset, offset + 4):
        if pos >= len(data):
            raise ValueError("Truncated VLQ sequence")
        b = data[pos]
        value = (value << 7) | (b & 0x7F)
        if not (b & 0x80):
            return value, pos - offset + 1
    raise ValueError("VLQ value exceeds 4 bytes")
