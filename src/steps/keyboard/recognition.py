"""Ambiguity-aware chord recognition from sounding MIDI notes.

The recogniser compares the played pitch-class set against every quality in
``CHORD_TEMPLATES`` on every root. It never invents a chord and never returns a
confidence number. Instead it returns *all* matching readings with explicit,
checkable reasons (root in bass, standard voicing omits the fifth, missing
tone, fits the key). Ordering is deterministic and documented, not a ranking of
musical truth: C-E-G-A stays both C6 and Am7/C.

Spelling of a recognised root is contextual: with a key the scale spelling is
used; without one the documented default table (sharps only for F#/C#, the same
table as ``theory.beginner_voicing``) is used and marked as such.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Literal, Optional

from ..theory.chord import CHORD_TEMPLATES, ChordDefinition
from ..theory.exceptions import MusicTheoryError
from ..theory.inversion import detect_chord_inversion
from ..theory.pitch import NoteSpelling
from ..theory.scale import ScaleDefinition
from .chord_tones import ChordToneRole, is_seventh_quality, render_chord_symbol, role_for_interval
from .model import sorted_unique_notes

Convention = Literal["INT", "DE"]

# Context-free default spelling per pitch class (same table as beginner_voicing).
_DEFAULT_SPELLINGS: tuple[tuple[str, int], ...] = (
    ("C", 0), ("C", 1), ("D", 0), ("E", -1), ("E", 0), ("F", 0),
    ("F", 1), ("G", 0), ("A", -1), ("A", 0), ("B", -1), ("B", 0),
)

_CATEGORY_ORDER = {"TRIAD": 0, "SUSPENDED": 1, "SEVENTH": 2, "ADD": 3, "EXTENDED": 4}


class RecognitionStatus(str, Enum):
    EMPTY = "EMPTY"
    SINGLE_NOTE = "SINGLE_NOTE"
    INTERVAL = "INTERVAL"
    EXACT_MATCH = "EXACT_MATCH"  # exactly one complete reading
    AMBIGUOUS = "AMBIGUOUS"  # several complete readings of the same pitch classes
    INCOMPLETE = "INCOMPLETE"  # no complete reading, but a chord missing one tone
    UNSUPPORTED = "UNSUPPORTED"  # no supported quality explains the notes


class CandidateKind(str, Enum):
    EXACT = "EXACT"  # all theoretical tones present, nothing extra
    STANDARD_VOICING = "STANDARD_VOICING"  # matches the template's default voiced selection
    INCOMPLETE = "INCOMPLETE"  # only the perfect fifth missing, root present, nothing extra


class Reason(str, Enum):
    ROOT_IN_BASS = "ROOT_IN_BASS"
    INVERSION_BASS = "INVERSION_BASS"  # bass is another chord tone (inversion)
    OMITS_FIFTH_BY_TEMPLATE = "OMITS_FIFTH_BY_TEMPLATE"
    MISSING_TONE = "MISSING_TONE"
    DOUBLED_TONES = "DOUBLED_TONES"
    ROOT_IN_KEY = "ROOT_IN_KEY"
    ALL_TONES_IN_KEY = "ALL_TONES_IN_KEY"
    TONES_OUTSIDE_KEY = "TONES_OUTSIDE_KEY"


SpellingBasis = Literal["KEY_CONTEXT", "DEFAULT_TABLE"]


@dataclass(frozen=True)
class ChordCandidate:
    chord: ChordDefinition  # includes a slash bass when the bass is not the root
    kind: CandidateKind
    reasons: tuple[Reason, ...]
    missing_roles: tuple[ChordToneRole, ...]
    bass_role: ChordToneRole
    figured_bass: str
    spelling_basis: SpellingBasis

    def symbol(self, convention: Convention = "INT") -> str:
        return render_chord_symbol(self.chord, convention)

    @property
    def fits_key(self) -> bool | None:
        if Reason.ALL_TONES_IN_KEY in self.reasons:
            return True
        if Reason.TONES_OUTSIDE_KEY in self.reasons:
            return False
        return None


@dataclass(frozen=True)
class RecognitionResult:
    notes: tuple[int, ...]
    pitch_classes: tuple[int, ...]
    status: RecognitionStatus
    candidates: tuple[ChordCandidate, ...]
    interval_semitones: Optional[int] = None  # for INTERVAL: lowest-to-highest distinct pcs (mod 12)

    @property
    def best_supported(self) -> Optional[ChordCandidate]:
        """First candidate in deterministic order; *not* a claim of the single correct reading."""
        return self.candidates[0] if self.candidates else None


def default_spelling(pitch_class: int, octave: int = 4) -> NoteSpelling:
    step, alteration = _DEFAULT_SPELLINGS[pitch_class % 12]
    return NoteSpelling(step, alteration, octave)  # type: ignore[arg-type]


def _context_spelling(pitch_class: int, key: Optional[ScaleDefinition]) -> tuple[NoteSpelling, SpellingBasis]:
    if key is not None:
        for spelling in key.spellings:
            if int(spelling.pitch_class) == pitch_class:
                return NoteSpelling(spelling.step, spelling.alteration, 4), "KEY_CONTEXT"
    return default_spelling(pitch_class), "DEFAULT_TABLE"


def _bass_spelling(root: NoteSpelling, root_quality: str, bass_pc: int, key: Optional[ScaleDefinition]) -> NoteSpelling:
    from .chord_tones import chord_tones  # local import avoids cycle at module import time

    for tone in chord_tones(ChordDefinition(root, root_quality)):
        if tone.pitch_class == bass_pc and tone.spelling is not None:
            return NoteSpelling(tone.spelling.step, tone.spelling.alteration, 3)
    spelling, _ = _context_spelling(bass_pc, key)
    return NoteSpelling(spelling.step, spelling.alteration, 3)


def recognize_chord(
    notes: Iterable[int],
    key: Optional[ScaleDefinition] = None,
    *,
    allow_incomplete: bool = True,
) -> RecognitionResult:
    """Return every supported reading of the sounding ``notes``.

    ``notes`` are MIDI numbers; duplicates are ignored (they are the same key).
    Octave doublings collapse to one pitch class but are reported as a reason.
    """
    raw = list(notes)
    played = sorted_unique_notes(raw)
    pcs = tuple(sorted({n % 12 for n in played}))
    if not played:
        return RecognitionResult((), (), RecognitionStatus.EMPTY, ())
    if len(pcs) == 1:
        return RecognitionResult(played, pcs, RecognitionStatus.SINGLE_NOTE, ())
    if len(pcs) == 2:
        low_pc = played[0] % 12
        other = next(pc for pc in pcs if pc != low_pc)
        return RecognitionResult(played, pcs, RecognitionStatus.INTERVAL, (), (other - low_pc) % 12)

    played_set = set(pcs)
    bass_pc = played[0] % 12
    doubled = len(played) > len(pcs)
    key_pcs = {int(s.pitch_class) for s in key.spellings} if key is not None else None
    found: list[tuple[tuple, ChordCandidate]] = []

    for quality, template in CHORD_TEMPLATES.items():
        theoretical = tuple(template["theoretical"])
        voiced = tuple(template["voiced"])
        for root_pc in range(12):
            full = {(root_pc + s) % 12 for s in theoretical}
            standard = {(root_pc + s) % 12 for s in voiced}
            if played_set == full:
                kind, missing_semis = CandidateKind.EXACT, ()
            elif played_set == standard and standard != full:
                kind = CandidateKind.STANDARD_VOICING
                missing_semis = tuple(s for s in theoretical if (root_pc + s) % 12 not in played_set)
            elif (
                allow_incomplete
                and played_set < full
                and full - played_set == {(root_pc + 7) % 12}
                and 7 in theoretical
                and root_pc in played_set
            ):
                # Only the perfect fifth may be absent: it is the conventional
                # omission. A missing third, seventh or alteration would change
                # the chord quality and is not offered as a reading.
                kind = CandidateKind.INCOMPLETE
                missing_semis = tuple(s for s in theoretical if (root_pc + s) % 12 not in played_set)
            else:
                continue
            candidate = _build_candidate(
                quality, root_pc, kind, missing_semis, played, bass_pc, doubled, key, key_pcs,
            )
            if candidate is None:
                continue
            order = (
                0 if kind is CandidateKind.EXACT else 1 if kind is CandidateKind.STANDARD_VOICING else 2,
                0 if root_pc == bass_pc else 1,
                _CATEGORY_ORDER.get(template["category"], 9),
                len(theoretical),
                (root_pc - bass_pc) % 12,
                quality,
            )
            found.append((order, candidate))

    found.sort(key=lambda item: item[0])
    candidates = tuple(candidate for _, candidate in found)
    complete = [c for c in candidates if c.kind is not CandidateKind.INCOMPLETE]
    if len(complete) == 1:
        status = RecognitionStatus.EXACT_MATCH
    elif len(complete) > 1:
        status = RecognitionStatus.AMBIGUOUS
    elif candidates:
        status = RecognitionStatus.INCOMPLETE
    else:
        status = RecognitionStatus.UNSUPPORTED
    if complete:
        candidates = tuple(complete) + tuple(c for c in candidates if c.kind is CandidateKind.INCOMPLETE)
    return RecognitionResult(played, pcs, status, candidates)


def _build_candidate(
    quality: str,
    root_pc: int,
    kind: CandidateKind,
    missing_semis: tuple[int, ...],
    played: tuple[int, ...],
    bass_pc: int,
    doubled: bool,
    key: Optional[ScaleDefinition],
    key_pcs: Optional[set[int]],
) -> Optional[ChordCandidate]:
    root, basis = _context_spelling(root_pc, key)
    try:
        bass = None if bass_pc == root_pc else _bass_spelling(root, quality, bass_pc, key)
        chord = ChordDefinition(root, quality, bass)
    except MusicTheoryError:
        return None
    reasons: list[Reason] = []
    if bass_pc == root_pc:
        reasons.append(Reason.ROOT_IN_BASS)
    else:
        reasons.append(Reason.INVERSION_BASS)
    if kind is CandidateKind.STANDARD_VOICING:
        reasons.append(Reason.OMITS_FIFTH_BY_TEMPLATE)
    if kind is CandidateKind.INCOMPLETE:
        reasons.append(Reason.MISSING_TONE)
    if doubled:
        reasons.append(Reason.DOUBLED_TONES)
    if key_pcs is not None:
        if root_pc in key_pcs:
            reasons.append(Reason.ROOT_IN_KEY)
        played_pcs = {n % 12 for n in played}
        reasons.append(Reason.ALL_TONES_IN_KEY if played_pcs <= key_pcs else Reason.TONES_OUTSIDE_KEY)
    bass_semitones = next(
        (s for s in CHORD_TEMPLATES[quality]["theoretical"] if (root_pc + s) % 12 == bass_pc), None,
    )
    bass_role = role_for_interval(quality, bass_semitones) if bass_semitones is not None else ChordToneRole.SLASH_BASS
    analysis = detect_chord_inversion(list(played), root_pitch_class=root_pc,
                                      is_seventh=is_seventh_quality(quality))
    return ChordCandidate(
        chord=chord,
        kind=kind,
        reasons=tuple(reasons),
        missing_roles=tuple(role_for_interval(quality, s) for s in missing_semis),
        bass_role=bass_role,
        figured_bass=analysis.figured_bass,
        spelling_basis=basis,
    )


__all__ = [
    "CandidateKind",
    "ChordCandidate",
    "Reason",
    "RecognitionResult",
    "RecognitionStatus",
    "default_spelling",
    "recognize_chord",
]
