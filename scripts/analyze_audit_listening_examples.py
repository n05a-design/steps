"""Measure the rendered Fable listening examples without using renderer internals."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import cos, pi, sqrt
from pathlib import Path
import struct
import wave


def tone_amplitude(samples, frequency, rate):
    """Project a PCM window onto a frequency with the Goertzel recurrence."""
    factor = 2 * cos(2 * pi * frequency / rate)
    previous = earlier = 0.0
    for sample in samples:
        earlier, previous = previous, sample + factor * previous - earlier
    energy = previous**2 + earlier**2 - factor * previous * earlier
    return 2 * sqrt(max(0, energy)) / (len(samples) * 32768)


def window(samples, rate, time, start, stop):
    return samples[round((time + start) * rate):round((time + stop) * rate)]


def measure_meter(samples, rate):
    cycle_count, pulses_per_cycle = 4, 12
    if len(samples) != rate * 8:
        raise ValueError("PAT-031 must contain four two-second cycles.")
    measurements = []
    for cycle in range(cycle_count):
        bell_positions = []
        marked_starts = []
        quarter_amplitudes = {}
        for pulse in range(pulses_per_cycle):
            time = (cycle * pulses_per_cycle + pulse) / 6
            frame = window(samples, rate, time, 0.012, 0.068)
            if tone_amplitude(frame, 988, rate) > 0.04:
                bell_positions.append(pulse)
            pulse_amplitude = tone_amplitude(frame, 137, rate)
            if pulse_amplitude > 0.08:
                quarter_amplitudes[pulse] = round(pulse_amplitude, 3)
            if pulse_amplitude > 0.20:
                marked_starts.append(pulse)
        measurements.append({
            "bell_eighth_positions": bell_positions,
            "pulse_amplitudes_by_eighth": quarter_amplitudes,
            "marked_eighth_positions": marked_starts,
        })
    return measurements


def midi_frequency(note):
    return 440 * 2 ** ((note - 69) / 12)


def measure_progression(samples, rate):
    if len(samples) != round(rate * 28.8):
        raise ValueError("PROG-001 must contain three 16-beat loops at 100 BPM.")
    loops = []
    for loop in range(3):
        chords, melody, accented_beats = [], [], []
        for beat in range(16):
            time = (16 * loop + beat) * 0.6
            if beat % 4 == 0:
                frame = window(samples, rate, time, 0.040, 0.570)
                chords.append([
                    note for note in range(40, 65)
                    if tone_amplitude(frame, midi_frequency(note), rate) > 0.035
                ])
            frame = window(samples, rate, time, 0.025, 0.370)
            amplitudes = [(tone_amplitude(frame, midi_frequency(note), rate), note)
                          for note in range(65, 80)]
            amplitude, note = max(amplitudes)
            if amplitude < 0.15:
                raise ValueError(f"No clear melody tone in loop {loop + 1}, beat {beat + 1}.")
            melody.append(note)
            if amplitude > 0.25:
                accented_beats.append(beat)
        loops.append({
            "chord_midi": chords,
            "melody_midi": melody,
            "accented_quarter_positions": accented_beats,
        })
    return loops


def analyze(path, measure):
    with wave.open(str(path), "rb") as sound:
        if (sound.getnchannels(), sound.getsampwidth(), sound.getcomptype()) != (1, 2, "NONE"):
            raise ValueError(f"{path.name}: expected mono PCM16 WAV.")
        frame_count = sound.getnframes()
        rate = sound.getframerate()
        samples = struct.unpack(f"<{frame_count}h", sound.readframes(frame_count))
    return {
        "sha256": sha256(path.read_bytes()).hexdigest(),
        "sample_rate_hz": rate,
        "frames": frame_count,
        "measurements": measure(samples, rate),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    results = {}
    try:
        for prefix, measure in (("pat-031", measure_meter), ("prog-001", measure_progression)):
            for variant in ("a", "b"):
                name = f"{prefix}-{variant}.wav"
                results[name] = analyze(directory / name, measure)
    except (OSError, ValueError, EOFError, struct.error, wave.Error) as exc:
        parser.exit(1, f"Audio analysis failed: {exc}\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
