"""Semantic key states, overlay priority and the renderer-neutral keyboard view model.

A key can carry several facts at once (chord tone, scale tone, pressed, practice
target). The view model keeps *all* of them in ``states`` and additionally
derives three display channels with a fixed, documented priority so no fact is
silently overwritten:

* ``fill``    – the single strongest state (practice feedback > input > chord > scale),
* ``outline`` – scale membership whenever ``fill`` is not already a scale state,
* ``badges``  – text markers (role label, root, bass, comparison) so nothing
  depends on colour alone (WCAG 1.4.1).

No colour values live here; a view maps ``KeyState`` names to theme tokens.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Literal, Optional, Sequence

from ..theory.pitch import NoteSpelling
from .chord_tones import ChordToneRole, strip_octave
from .model import KeyboardViewport, PianoKey, is_on_piano, sorted_unique_notes

Convention = Literal["INT", "DE"]


class KeyState(str, Enum):
    PRACTICE_WRONG = "PRACTICE_WRONG"
    PRACTICE_MISSING = "PRACTICE_MISSING"
    PRACTICE_CORRECT = "PRACTICE_CORRECT"
    PRESSED = "PRESSED"
    SELECTED = "SELECTED"
    CHORD_ROOT = "CHORD_ROOT"
    CHORD_TONE = "CHORD_TONE"
    CHORD_BASS = "CHORD_BASS"
    COMPARISON = "COMPARISON"
    COMPARISON_HELD = "COMPARISON_HELD"
    SCALE_ROOT = "SCALE_ROOT"
    SCALE_TONE = "SCALE_TONE"


# Highest priority first. CHORD_BASS is marker-only (badge), never a fill.
FILL_PRIORITY: tuple[KeyState, ...] = (
    KeyState.PRACTICE_WRONG,
    KeyState.PRACTICE_MISSING,
    KeyState.PRACTICE_CORRECT,
    KeyState.PRESSED,
    KeyState.SELECTED,
    KeyState.CHORD_ROOT,
    KeyState.CHORD_TONE,
    KeyState.COMPARISON_HELD,
    KeyState.COMPARISON,
    KeyState.SCALE_ROOT,
    KeyState.SCALE_TONE,
)
_SCALE_STATES = (KeyState.SCALE_ROOT, KeyState.SCALE_TONE)


@dataclass(frozen=True)
class KeyVisual:
    key: PianoKey
    states: frozenset[KeyState]
    fill: Optional[KeyState]
    outline: Optional[KeyState]
    badges: tuple[str, ...]  # e.g. ("1", "R"), ("b7",), ("B",)
    label: str  # contextual note name (with octave) or "" when no context spells it
    description: str  # plain-text state summary codes, joined by ", " (for screen readers / tooltips)

    @property
    def midi(self) -> int:
        return self.key.midi


@dataclass(frozen=True)
class KeyboardViewModel:
    viewport: KeyboardViewport
    keys: tuple[KeyVisual, ...]
    hidden_below: tuple[int, ...]  # musical notes left of the visible range (still on piano or not)
    hidden_above: tuple[int, ...]
    off_piano: tuple[int, ...]  # valid MIDI but outside A0..C8
    title: str = ""
    lines: tuple[str, ...] = ()

    def visual(self, midi: int) -> KeyVisual:
        for item in self.keys:
            if item.key.midi == midi:
                return item
        raise KeyError(midi)


@dataclass
class KeyboardLayers:
    """Everything that may be highlighted, independent of what is visible."""

    chord_notes: dict[int, ChordToneRole] = field(default_factory=dict)  # concrete voicing MIDI -> role
    chord_bass: Optional[int] = None
    spellings: dict[int, NoteSpelling] = field(default_factory=dict)  # MIDI -> contextual spelling
    scale_pitch_classes: dict[int, int] = field(default_factory=dict)  # pc -> degree (1-based)
    scale_spellings: dict[int, NoteSpelling] = field(default_factory=dict)  # pc -> spelling
    comparison_notes: frozenset[int] = frozenset()
    comparison_held: frozenset[int] = frozenset()
    pressed: frozenset[int] = frozenset()
    selected: frozenset[int] = frozenset()
    practice_correct: frozenset[int] = frozenset()
    practice_wrong: frozenset[int] = frozenset()
    practice_missing: frozenset[int] = frozenset()

    def musical_notes(self) -> tuple[int, ...]:
        """Absolute pitches that must not disappear just because they are off-screen."""
        return sorted_unique_notes(
            [*self.chord_notes, *self.comparison_notes, *self.pressed, *self.selected,
             *self.practice_correct, *self.practice_wrong, *self.practice_missing]
        )


def states_for(midi: int, layers: KeyboardLayers) -> frozenset[KeyState]:
    states: set[KeyState] = set()
    role = layers.chord_notes.get(midi)
    if role is not None:
        states.add(KeyState.CHORD_ROOT if role is ChordToneRole.ROOT else KeyState.CHORD_TONE)
    if layers.chord_bass == midi:
        states.add(KeyState.CHORD_BASS)
    degree = layers.scale_pitch_classes.get(midi % 12)
    if degree is not None:
        states.add(KeyState.SCALE_ROOT if degree == 1 else KeyState.SCALE_TONE)
    for flag, collection in (
        (KeyState.COMPARISON_HELD, layers.comparison_held),
        (KeyState.COMPARISON, layers.comparison_notes),
        (KeyState.PRESSED, layers.pressed),
        (KeyState.SELECTED, layers.selected),
        (KeyState.PRACTICE_CORRECT, layers.practice_correct),
        (KeyState.PRACTICE_WRONG, layers.practice_wrong),
        (KeyState.PRACTICE_MISSING, layers.practice_missing),
    ):
        if midi in collection:
            states.add(flag)
    if KeyState.COMPARISON_HELD in states:
        states.discard(KeyState.COMPARISON)
    return frozenset(states)


def resolve_fill(states: Iterable[KeyState]) -> Optional[KeyState]:
    present = set(states)
    return next((state for state in FILL_PRIORITY if state in present), None)


def resolve_outline(states: Iterable[KeyState], fill: Optional[KeyState]) -> Optional[KeyState]:
    present = set(states)
    if fill in _SCALE_STATES:
        return None
    return next((state for state in _SCALE_STATES if state in present), None)


def build_view_model(
    viewport: KeyboardViewport,
    layers: KeyboardLayers,
    convention: Convention,
    *,
    title: str = "",
    lines: Sequence[str] = (),
    show_all_names: bool = False,
) -> KeyboardViewModel:
    keys: list[KeyVisual] = []
    for key in viewport.keys():
        midi = key.midi
        states = states_for(midi, layers)
        fill = resolve_fill(states)
        outline = resolve_outline(states, fill)
        badges: list[str] = []
        role = layers.chord_notes.get(midi)
        if role is not None:
            badges.append(role.interval_label)
        if KeyState.CHORD_BASS in states:
            badges.append("B")
        if KeyState.COMPARISON_HELD in states:
            badges.append("=")
        elif KeyState.COMPARISON in states:
            badges.append("·")
        if KeyState.PRACTICE_WRONG in states:
            badges.append("✗")
        elif KeyState.PRACTICE_MISSING in states:
            badges.append("?")
        elif KeyState.PRACTICE_CORRECT in states:
            badges.append("✓")
        label = _label(key, layers, convention, show_all_names)
        description = ", ".join(sorted(state.value for state in states))
        keys.append(KeyVisual(key, states, fill, outline, tuple(badges), label, description))
    notes = layers.musical_notes()
    off_piano = tuple(n for n in notes if not is_on_piano(n))
    below, _, above = viewport.partition(n for n in notes if is_on_piano(n))
    return KeyboardViewModel(viewport, tuple(keys), below, above, off_piano, title, tuple(lines))


def _label(key: PianoKey, layers: KeyboardLayers, convention: Convention, show_all: bool) -> str:
    midi = key.midi
    spelling = layers.spellings.get(midi)
    if spelling is None:
        pc_spelling = layers.scale_spellings.get(midi % 12)
        if pc_spelling is not None:
            octave = pc_spelling.octave + (midi - pc_spelling.midi_number) // 12
            spelling = NoteSpelling(pc_spelling.step, pc_spelling.alteration, octave)
    if spelling is not None:
        return spelling.render(convention)
    if key.is_white and (show_all or key.pitch_class == 0):
        return key.enharmonic_spellings()[0].render(convention)
    if show_all and key.is_black:
        sharps = [s for s in key.enharmonic_spellings() if abs(s.alteration) == 1]
        return "/".join(strip_octave(s.render(convention)) for s in sharps)
    return ""


def practice_layers(expected: Iterable[int], played: Iterable[int], exact: bool) -> dict[str, frozenset[int]]:
    """Map practice feedback to keys. Pitch-class tasks mark keys by pitch class."""
    expected_notes = set(sorted_unique_notes(expected))
    played_notes = set(sorted_unique_notes(played))
    if exact:
        correct = played_notes & expected_notes
        wrong = played_notes - expected_notes
        missing = expected_notes - played_notes
    else:
        expected_pcs = {n % 12 for n in expected_notes}
        played_pcs = {n % 12 for n in played_notes}
        correct = {n for n in played_notes if n % 12 in expected_pcs}
        wrong = {n for n in played_notes if n % 12 not in expected_pcs}
        missing = {n for n in expected_notes if n % 12 not in played_pcs}
    return {"correct": frozenset(correct), "wrong": frozenset(wrong), "missing": frozenset(missing)}


__all__ = [
    "FILL_PRIORITY",
    "KeyState",
    "KeyVisual",
    "KeyboardLayers",
    "KeyboardViewModel",
    "build_view_model",
    "practice_layers",
    "resolve_fill",
    "resolve_outline",
    "states_for",
]
