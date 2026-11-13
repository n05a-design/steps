"""Render original listening controls for PAT-031 and PROG-001 as mono WAV."""

from __future__ import annotations

import argparse
from array import array
from math import exp, pi, sin
from pathlib import Path
import sys
import wave

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.steps.theory import midi_to_frequency

SAMPLE_RATE = 22050
BELL_PULSES = (0, 2, 4, 5, 7, 9, 11)
POP_CHORDS = ((48, 55, 60, 64), (43, 55, 59, 62), (45, 52, 57, 60), (41, 53, 57, 60))
POP_MELODIES = {
    "c": (72, 76, 79, 76, 74, 71, 74, 74, 72, 76, 72, 69, 69, 65, 67, 72),
    "a": (69, 72, 76, 72, 71, 74, 71, 74, 69, 72, 76, 69, 72, 65, 67, 69),
}


def add_tone(samples, start, length, frequency, gain, decay):
    first = round(start * SAMPLE_RATE)
    stop = min(round((start + length) * SAMPLE_RATE), len(samples))
    for frame in range(first, stop):
        elapsed = (frame - first) / SAMPLE_RATE
        envelope = min(elapsed / 0.006, 1.0, (stop - frame) / (0.020 * SAMPLE_RATE))
        samples[frame] += gain * envelope * exp(-elapsed * decay) * sin(2 * pi * frequency * elapsed)


def meter_audio(bar_starts):
    # 120 dotted-quarter beats/minute, three eighths per beat.
    pulse = 0.5 / 3
    samples = [0.0] * (SAMPLE_RATE * 8)
    for cycle in range(4):
        for index in BELL_PULSES:
            time = (12 * cycle + index) * pulse
            add_tone(samples, time, 0.11, 988.0, 0.22, 25)
            add_tone(samples, time, 0.08, 1489.0, 0.10, 40)
        for index in range(0, 12, 3):
            time = (12 * cycle + index) * pulse
            accented = index in bar_starts
            add_tone(samples, time, 0.16, 137.0, 0.47 if accented else 0.19, 15)
    return samples


def pop_audio(melody):
    # Three identical 4/4 chord loops at quarter note = 100 BPM.
    beat = 0.6
    samples = [0.0] * round(SAMPLE_RATE * beat * 16 * 3)
    for loop in range(3):
        offset = loop * 16
        for measure, chord in enumerate(POP_CHORDS):
            for pitch in chord:
                add_tone(samples, (offset + 4 * measure) * beat, 3.9 * beat,
                         midi_to_frequency(pitch), 0.075, 1.3)
        for index, pitch in enumerate(melody):
            duration = 0.96 if index in (0, 8, 15) else 0.66
            add_tone(samples, (offset + index) * beat, duration * beat,
                     midi_to_frequency(pitch), 0.43 if index in (0, 8, 15) else 0.32, 1.8)
    return samples


def write_wave(path, samples):
    pcm = array("h", (round(max(-1.0, min(1.0, sample)) * 32767) for sample in samples))
    if sys.byteorder != "little":
        pcm.byteswap()
    with path.open("xb") as file, wave.open(file, "wb") as sound:
        sound.setparams((1, 2, SAMPLE_RATE, 0, "NONE", "not compressed"))
        sound.writeframes(pcm.tobytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    examples = (
        ("pat-031-a", meter_audio, (0,)),
        ("pat-031-b", meter_audio, (0, 6)),
        ("prog-001-a", pop_audio, POP_MELODIES["c"]),
        ("prog-001-b", pop_audio, POP_MELODIES["a"]),
    )
    for name, _, _ in examples:
        path = args.output_dir / f"{name}.wav"
        if path.exists() or path.is_symlink():
            parser.exit(1, f"Output already exists: {path}\n")
    for name, generator, control in examples:
        path = args.output_dir / f"{name}.wav"
        write_wave(path, generator(control))
        print(path)


if __name__ == "__main__":
    main()
