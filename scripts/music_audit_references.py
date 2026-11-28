"""Independent 12-TET candidate profile from the MVVE V2 handoff.

The symbol vocabulary and six provisional conventions match the handoff.
These formulas are test inputs and do not constitute reviewed learning content.
"""

from collections import defaultdict
from itertools import accumulate
import random
import re

PROFILE = "mvve-v2-12tet-candidate-1"
ROOTS = ("C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")
LETTERS = "CDEFGAB"
MAJOR = (0, 2, 4, 5, 7, 9, 11)
FORMULAS = {
    "": "1 3 5", "m": "1 b3 5", "dim": "1 b3 b5", "(b5)": "1 3 b5", "aug": "1 3 #5",
    "sus4": "1 4 5", "sus2": "1 2 5", "add9": "1 3 5 9", "madd9": "1 b3 5 9",
    "6": "1 3 5 6", "m6": "1 b3 5 6", "7": "1 3 5 b7", "maj7": "1 3 5 7", "m7": "1 b3 5 b7",
    "m7b5": "1 b3 b5 b7", "dim7": "1 b3 b5 bb7", "m(maj7)": "1 b3 5 7",
    "7#5": "1 3 #5 b7", "maj7#5": "1 3 #5 7", "7sus4": "1 4 5 b7",
    "9": "1 3 5 b7 9", "maj9": "1 3 5 7 9", "m9": "1 b3 5 b7 9",
    "7b9": "1 3 5 b7 b9", "7#9": "1 3 5 b7 #9", "7#11": "1 3 5 b7 #11",
    "7b5": "1 3 b5 b7", "7b13": "1 3 5 b7 b13", "13": "1 3 5 b7 9 13",
    "maj13": "1 3 5 7 9 13", "m11": "1 b3 5 b7 9 11",
}
PROFILE_REVIEW = {"13", "maj13", "7#11", "7b13", "add9", "7#9"}
MODES = ("ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian", "locrian")
MAJOR_STEPS = (2, 2, 1, 2, 2, 2, 1)
STEPS = {mode: MAJOR_STEPS[i:] + MAJOR_STEPS[:i] for i, mode in enumerate(MODES)}
STEPS.update({
    "harmonic_minor": (2, 1, 2, 2, 1, 3, 1), "melodic_minor": (2, 1, 2, 2, 2, 2, 1),
    "major_pentatonic": (2, 2, 3, 2, 3), "minor_pentatonic": (3, 2, 2, 3, 2),
    "blues": (3, 2, 1, 1, 3, 2), "whole_tone": (2,) * 6,
    "diminished_half_whole": (1, 2) * 4, "diminished_whole_half": (2, 1) * 4,
})


def natural_offset(index):
    return MAJOR[index % 7] + 12 * (index // 7)


def chord_formula(quality):
    result = []
    for token in FORMULAS[quality].split():
        accidental, degree = re.fullmatch(r"([b#]*)([1-9][0-9]*)", token).groups()
        index = int(degree) - 1
        result.append((token, index, natural_offset(index) + accidental.count("#") - accidental.count("b")))
    return result


def spell(root, letters, distance):
    index = LETTERS.index(root[0])
    target = natural_offset(index) + root.count("#") - root.count("b") + distance
    letter_index = index + letters
    alteration = target - natural_offset(letter_index)
    return LETTERS[letter_index % 7] + "#" * alteration + "b" * -alteration


def pitch_classes(mask):
    return tuple(pc for pc in range(12) if mask & (1 << pc))


def mask_bass_pairs():
    yield 0, None
    for mask in range(1, 1 << 12):
        for bass in pitch_classes(mask):
            yield mask, bass


def self_test():
    """Check fixed anchors even under Python -O."""
    pairs = set(mask_bass_pairs())
    checks = {
        "mask-bass cardinality": len(pairs) == 24577 and len({mask for mask, _ in pairs}) == 4096,
        "major triad": [semitones for _, _, semitones in chord_formula("")] == [0, 4, 7],
        "altered ninth": chord_formula("7#9")[-1] == ("#9", 8, 15) and spell("C", 8, 15) == "D#",
        "diminished seventh": spell("C", 6, 9) == "Bbb",
        "F sharp leading tone": spell("F#", 6, 11) == "E#",
        "scale closure": all(sum(steps) == 12 for steps in STEPS.values()),
    }
    failures = [name for name, passed in checks.items() if not passed]
    if failures:
        raise ValueError(", ".join(failures))
    return len(checks)


def cases(area, profile, seed):
    """Yield (stable ID, concrete input, independent expected result)."""
    if area == "pitch":
        for midi in range(128):
            spellings = [
                [letter, accidental, octave]
                for octave in range(-2, 11)
                for letter, base in zip(LETTERS, MAJOR, strict=True)
                for accidental in range(-2, 3)
                if 12 * (octave + 1) + base + accidental == midi
            ]
            yield f"PITCH-{midi:03}", {"midi": midi}, [
                midi, midi % 12, midi // 12 - 1, midi - 20 if 21 <= midi <= 108 else None,
                midi % 12 in (1, 3, 6, 8, 10), sorted(spellings),
            ]
        return
    if area == "chord-reference":
        for quality in FORMULAS:
            formula = chord_formula(quality)
            for pc, root in enumerate(ROOTS):
                expected = [[role, distance, (pc + distance) % 12, spell(root, index, distance)]
                            for role, index, distance in formula]
                yield f"REF-CHORD-{quality or 'major'}-{pc:02}", {
                    "symbol": root + quality, "convention_review_required": quality in PROFILE_REVIEW,
                }, expected
        return
    if area == "declared-bass":
        for quality in FORMULAS:
            formula = chord_formula(quality)
            factors = {distance % 12: (role, index, distance) for role, index, distance in formula}
            is_seventh = any(index == 6 for _, index, _ in formula)
            figures = {1: "7", 3: "6/5", 5: "4/3", 7: "4/2"} if is_seventh else {
                1: "5/3", 3: "6", 5: "6/4",
            }
            for pc, root in enumerate(ROOTS):
                chord_pcs = {(pc + distance) % 12 for distance in factors}
                for bass, name in enumerate(ROOTS):
                    factor = factors.get((bass - pc) % 12)
                    if factor is None:
                        role, figure = "/", "slash"
                    else:
                        role, index, distance = factor
                        name = spell(root, index, distance)
                        degree = index + 1
                        figure = figures.get(degree)
                        if degree in (2, 4):
                            figure = "slash"
                    notes = [36 + bass, *(60 + pc for pc in sorted(chord_pcs - {bass}))]
                    yield f"REF-BASS-{quality or 'major'}-{pc:02}-{bass:02}", {
                        "symbol": f"{root}{quality}/{name}", "notes": notes,
                    }, [role, figure, bass]
        return
    if area in ("scale-reference", "harmonization"):
        for name, steps in STEPS.items():
            offsets = (0, *list(accumulate(steps))[:-1])
            for pc, root in enumerate(ROOTS):
                notes = [(pc + offset) % 12 for offset in offsets]
                written = [spell(root, i, offset) for i, offset in enumerate(offsets)]
                if area == "scale-reference":
                    yield f"REF-SCALE-{name}-{pc:02}", {"root": root, "scale": name}, [
                        notes, list(offsets), written if len(offsets) == 7 else None,
                    ]
                elif len(offsets) == 7:
                    for degree in range(7):
                        for size in (3, 4):
                            indices = [degree + 2 * i for i in range(size)]
                            semitones = [offsets[i % 7] + 12 * (i // 7) for i in indices]
                            yield f"REF-HARM-{name}-{pc:02}-{degree + 1}-{size}", {
                                "root": root, "scale": name, "degree": degree + 1, "size": size,
                            }, [[offset - semitones[0] for offset in semitones],
                                sorted((pc + offset) % 12 for offset in semitones),
                                [spell(root, i, offset) for i, offset in zip(indices, semitones, strict=True)]]
        return
    if area != "recognition-exact":
        raise ValueError(area)
    by_mask = defaultdict(list)
    for root in range(12):
        for quality in FORMULAS:
            mask = sum(1 << ((root + semitones) % 12) for _, _, semitones in chord_formula(quality))
            by_mask[mask].append([root, quality])
    domain = tuple(mask_bass_pairs())
    if profile in ("smoke", "pr"):
        anchors = {(mask, bass) for mask, bass in domain if mask in by_mask or mask == 0}
        sample = random.Random(seed).sample(domain, 512 if profile == "smoke" else 1024)
        domain = sorted(anchors | set(sample))
    for mask, bass in domain:
        notes = [] if bass is None else [36 + bass, *(60 + pc for pc in pitch_classes(mask) if pc != bass)]
        yield f"RECOG-{mask:03x}-{bass}", {"notes": notes}, sorted(by_mask.get(mask, []))


AREAS = ("pitch", "chord-reference", "scale-reference", "harmonization", "declared-bass", "recognition-exact")
