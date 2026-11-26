"""Keyboard dialog: progression preview, free chord input and the practice pilot.

The dialog renders a ``KeyboardWorkbench`` (src/steps/keyboard). It never edits
the project directly; the single project change it offers ("add recognised
chord") goes through ``ProgressionSessionController.add_chord`` and is therefore
undoable like every other edit.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from app.i18n import LocaleManager
from app.ui.dialog_support import ModalDialog, configure_readonly_preview
from app.ui.keyboard_view import PianoKeyboardCanvas
from app.ui.session_controller import ProgressionSessionController
from app.ui.theme import ThemeManager, apply_window_geometry, create_button
from glide_shell.custom_controls import ThemedAutoScrollbar
from src.steps.keyboard.chord_tones import ChordToneRole, strip_octave
from src.steps.keyboard.input import InputSource
from src.steps.keyboard.practice import EvaluationPolicy
from src.steps.keyboard.recognition import CandidateKind, RecognitionStatus, default_spelling
from src.steps.keyboard.workbench import (
    KEY_SCALE,
    VOICING_TYPES,
    KeyboardMode,
    KeyboardWorkbench,
    available_scales,
)
from src.steps.theory.exceptions import MusicTheoryError

MODES = (KeyboardMode.PROGRESSION, KeyboardMode.FREE_INPUT, KeyboardMode.PRACTICE)
# Two rows of a typical computer keyboard, starting at the lowest visible C.
COMPUTER_KEYS = ("a", "w", "s", "e", "d", "f", "t", "g", "y", "h", "u", "j", "k")
_LAYOUT_ALIASES = {"z": "y"}  # QWERTZ: the key right of T maps like QWERTY "y"


def _note_name(note, convention: str) -> str:
    return note.name(convention) if note is not None else "?"


def _figure(figured_bass: str, translate: Callable[..., str]) -> str:
    """Core figured-bass text; the core marks non-chord-tone basses with 'slash'."""
    return translate("keyboard.figure.none") if figured_bass == "slash" else figured_bass


def describe_workbench(workbench: KeyboardWorkbench, translate: Callable[..., str]) -> str:
    """Plain-text, localized description of everything the keyboard shows."""
    convention = workbench.convention
    lines: list[str] = []
    model = workbench.view_model()
    if workbench.mode is KeyboardMode.PROGRESSION:
        info = workbench.chord_info()
        if info is None:
            return translate("keyboard.info.no_chords")
        lines.append(translate(
            "keyboard.info.chord", number=info.index + 1, symbol=info.symbol,
            roman=info.roman or translate("keyboard.info.roman_unavailable"),
        ))
        mode_key = "context.minor" if info.key_is_minor else "context.major"
        lines.append(translate("keyboard.info.key", key=f"{info.key_root} {translate(mode_key)}"))
        tones = ", ".join(f"{tone.name(convention)} ({tone.role.interval_label})" for tone in info.tones)
        lines.append(translate("keyboard.info.tones", tones=tones))
        if info.voicing is None:
            # The core error text is English; only a localized message is shown.
            lines.append(translate("keyboard.info.voicing_error", symbol=info.symbol))
        else:
            voicing = info.voicing
            notes = ", ".join(
                f"{note.name(convention)} ({note.midi})" for note in voicing.notes
            )
            lines.append(translate(
                "keyboard.info.voicing", type=translate(f"keyboard.voicing.{info.voicing_type}"),
                rotation=info.rotation, notes=notes,
            ))
            root = strip_octave(info.chord.root.render(convention))
            lines.append(translate("keyboard.info.root_bass", root=root, bass=_note_name(voicing.bass, convention)))
            if voicing.inversion is not None:
                inversion = voicing.inversion
                bass_role = voicing.bass.role
                if bass_role in (ChordToneRole.SLASH_BASS, ChordToneRole.NON_CHORD_TONE):
                    position = translate("keyboard.inversion.slash")
                elif inversion.bass_factor in ("SUSPENSION", "NON_CHORD_TONE"):
                    position = translate("keyboard.inversion.other_tone", role=bass_role.interval_label)
                else:
                    position = translate(f"keyboard.inversion.{inversion.inversion.value}")
                if info.rotation and info.chord.bass is not None:
                    lines.append(translate("keyboard.info.rotation_slash", symbol=info.symbol))
                lines.append(translate(
                    "keyboard.info.inversion", position=position, figure=_figure(inversion.figured_bass, translate),
                ))
            if voicing.omitted_roles:
                lines.append(translate(
                    "keyboard.info.omitted", roles=", ".join(r.interval_label for r in voicing.omitted_roles),
                ))
        if workbench.compare_previous:
            lines.extend(_comparison_lines(workbench, translate))
        lines.append(translate("keyboard.info.preview_only"))
    elif workbench.mode is KeyboardMode.FREE_INPUT:
        lines.extend(_recognition_lines(workbench, translate))
    else:
        lines.extend(_practice_lines(workbench, translate))
    if workbench.show_scale:
        scale = workbench.overlay_scale()
        if scale is not None:
            names = ", ".join(strip_octave(s.render(convention)) for s in scale.spellings)
            lines.append(translate(
                "keyboard.info.scale",
                scale=f"{strip_octave(scale.root.render(convention))} {translate(f'keyboard.scale.{scale.name}')}",
                notes=names,
            ))
    if model.hidden_below or model.hidden_above:
        lines.append(translate("keyboard.info.hidden", below=len(model.hidden_below), above=len(model.hidden_above)))
    if model.off_piano:
        lines.append(translate("keyboard.info.off_piano", notes=", ".join(map(str, model.off_piano))))
    return "\n".join(lines)


def _comparison_lines(workbench: KeyboardWorkbench, translate: Callable[..., str]) -> list[str]:
    comparison = workbench.comparison()
    if comparison is None:
        return [translate("keyboard.compare.none")]
    previous = workbench.session.chords[(workbench.selected_index or 1) - 1]
    lines = [translate("keyboard.compare.header", symbol=previous)]
    if comparison.paired:
        for motion in comparison.motions:
            lines.append("  " + translate(
                "keyboard.compare.voice", voice=motion.voice + 1, start=motion.start, end=motion.end,
                steps=f"{motion.semitones:+d}" if motion.semitones else "0",
                motion=translate(f"keyboard.motion.{motion.kind.value}.{motion.direction.value}"),
            ))
        lines.append("  " + translate("keyboard.compare.total", total=comparison.total_movement))
    else:
        lines.append("  " + translate("keyboard.compare.unpaired"))
    lines.append("  " + translate(
        "keyboard.compare.sets",
        held=", ".join(map(str, comparison.held_pitches)) or "–",
        added=", ".join(map(str, comparison.added_pitches)) or "–",
        removed=", ".join(map(str, comparison.removed_pitches)) or "–",
    ))
    return lines


def _recognition_lines(workbench: KeyboardWorkbench, translate: Callable[..., str]) -> list[str]:
    result = workbench.recognition()
    convention = workbench.convention
    lines = [translate("keyboard.input.notes", notes=", ".join(map(str, result.notes)) or "–")]
    lines.append(translate(f"keyboard.recognition.{result.status.value}"))
    if result.status is RecognitionStatus.INTERVAL:
        lines.append(translate("keyboard.recognition.interval_size", semitones=result.interval_semitones))
    for candidate in result.candidates[:8]:
        reasons = ", ".join(translate(f"keyboard.reason.{reason.value}") for reason in candidate.reasons)
        lines.append("  • " + translate(
            "keyboard.recognition.candidate", symbol=candidate.symbol(convention),
            kind=translate(f"keyboard.candidate.{candidate.kind.value}"),
            figure=_figure(candidate.figured_bass, translate), reasons=reasons,
        ))
        if candidate.missing_roles:
            lines.append("    " + translate(
                "keyboard.recognition.missing", roles=", ".join(r.interval_label for r in candidate.missing_roles),
            ))
    if len(result.candidates) > 8:
        lines.append(translate("keyboard.recognition.more", count=len(result.candidates) - 8))
    if result.candidates and result.candidates[0].spelling_basis == "DEFAULT_TABLE":
        lines.append(translate("keyboard.recognition.default_spelling"))
    if result.status is RecognitionStatus.AMBIGUOUS:
        lines.append(translate("keyboard.recognition.ambiguity_note"))
    return lines


def _practice_lines(workbench: KeyboardWorkbench, translate: Callable[..., str]) -> list[str]:
    exercise = workbench.exercise
    lines = [
        translate("keyboard.practice.pilot_status"),
        translate("keyboard.practice.task", number=workbench.exercise_index + 1,
                  total=len(workbench.exercises), task=translate(exercise.prompt_key)),
        translate("keyboard.practice.objective", objective=translate(exercise.objective_key)),
        translate(f"keyboard.practice.policy.{exercise.policy.value}"),
    ]
    feedback = workbench.feedback
    if feedback is not None:
        lines.append(translate(feedback.message_key))
        convention = workbench.convention
        if exercise.policy is EvaluationPolicy.EXACT_PITCHES:
            lines.append(translate(
                "keyboard.practice.detail_pitches",
                missing=", ".join(map(str, feedback.missing_pitches)) or "–",
                extra=", ".join(map(str, feedback.extra_pitches)) or "–",
            ))
        else:
            def names(pcs):
                return ", ".join(strip_octave(default_spelling(pc).render(convention)) for pc in pcs) or "–"
            lines.append(translate(
                "keyboard.practice.detail_tones",
                missing=names(feedback.missing_pitch_classes), extra=names(feedback.extra_pitch_classes),
            ))
            if feedback.bass_correct is False:
                lines.append(translate("keyboard.practice.detail_bass"))
    if workbench.show_practice_solution:
        for hint in exercise.hint_keys:
            lines.append(translate(hint))
    return lines


class KeyboardDialog(ModalDialog):
    """Modal keyboard workspace bound to the active progression controller."""

    def __init__(
        self,
        parent: tk.Misc,
        controller: ProgressionSessionController,
        i18n: LocaleManager,
        theme: ThemeManager,
        on_project_change: Callable[[int], None],
        selected_index: Optional[int] = None,
    ) -> None:
        self._controller = controller
        self._i18n = i18n
        self._theme = theme
        self._on_project_change = on_project_change
        self._colors = theme.colors
        self._font = (theme.typography.font_family_sans, theme.typography.size_sm)
        self.workbench = KeyboardWorkbench(lambda: controller.session)
        if selected_index is not None and 0 <= selected_index < len(controller.session.chords):
            self.workbench.selected_index = selected_index
        self._revision = controller.revision
        self._held_computer_keys: dict[str, int] = {}  # lower-case keysym -> note it pressed
        self._candidates: tuple = ()
        self._refreshing = False
        colors, spacing, t = self._colors, theme.spacing, i18n.translate

        super().__init__(parent)
        self.window.title(t("keyboard.title"))
        apply_window_geometry(self.window, 980, 640, 720, 500)
        self.window.configure(bg=colors.bg_window)
        container = tk.Frame(self.window, bg=colors.bg_window, padx=spacing.md, pady=spacing.md)
        container.pack(fill=tk.BOTH, expand=True)
        self._container = container

        def label(parent, key):
            return tk.Label(parent, text=t(key), bg=colors.bg_surface, fg=colors.text_primary, font=self._font)

        top_card = theme.make_surface_card(container, radius=theme.corner_radius, padding=spacing.xs, auto_height=True)
        top_card.pack(fill=tk.X, pady=(0, spacing.sm))
        row1 = tk.Frame(top_card.inner, bg=colors.bg_surface)
        row1.pack(fill=tk.X)
        label(row1, "keyboard.mode").pack(side=tk.LEFT, padx=(0, spacing.xs))
        self.mode_selector = ttk.Combobox(
            row1, state="readonly", width=21, font=self._font,
            values=tuple(t(f"keyboard.mode.{mode.value}") for mode in MODES),
        )
        self.mode_selector.current(0)
        self.mode_selector.pack(side=tk.LEFT)
        self.mode_selector.bind("<<ComboboxSelected>>", lambda _e: self._on_mode())
        label(row1, "keyboard.event").pack(side=tk.LEFT, padx=(spacing.sm, spacing.xs))
        self.prev_btn = create_button(row1, text=t("keyboard.previous"), command=lambda: self._step(-1),
                                      bg=colors.bg_active, fg=colors.text_primary)
        self.prev_btn.pack(side=tk.LEFT)
        self.event_selector = ttk.Combobox(row1, state="readonly", width=18, font=self._font)
        self.event_selector.pack(side=tk.LEFT, padx=spacing.xs)
        self.event_selector.bind("<<ComboboxSelected>>", lambda _e: self._on_event())
        self.next_btn = create_button(row1, text=t("keyboard.next"), command=lambda: self._step(1),
                                      bg=colors.bg_active, fg=colors.text_primary)
        self.next_btn.pack(side=tk.LEFT)
        label(row1, "keyboard.voicing").pack(side=tk.LEFT, padx=(spacing.sm, spacing.xs))
        self.voicing_selector = ttk.Combobox(
            row1, state="readonly", width=12, font=self._font,
            values=tuple(t(f"keyboard.voicing.{v}") for v in VOICING_TYPES),
        )
        self.voicing_selector.current(0)
        self.voicing_selector.pack(side=tk.LEFT)
        self.voicing_selector.bind("<<ComboboxSelected>>", lambda _e: self._on_voicing())
        self.rotate_down_btn = create_button(row1, text=t("keyboard.inversion.down"),
                                             command=lambda: self._rotate(-1), bg=colors.bg_active,
                                             fg=colors.text_primary)
        self.rotate_down_btn.pack(side=tk.LEFT, padx=(spacing.xs, 0))
        self.rotate_up_btn = create_button(row1, text=t("keyboard.inversion.up"),
                                           command=lambda: self._rotate(1), bg=colors.bg_active,
                                           fg=colors.text_primary)
        self.rotate_up_btn.pack(side=tk.LEFT, padx=(spacing.xs, 0))

        row2 = tk.Frame(top_card.inner, bg=colors.bg_surface)
        row2.pack(fill=tk.X, pady=(spacing.xs, 0))
        self._vars: dict[str, tk.BooleanVar] = {}
        for name, key, initial in (
            ("chord", "keyboard.show_chord", True), ("scale", "keyboard.show_scale", False),
            ("compare", "keyboard.compare_previous", False), ("names", "keyboard.all_names", False),
        ):
            var = tk.BooleanVar(master=self.window, value=initial)
            self._vars[name] = var
            tk.Checkbutton(
                row2, text=t(key), variable=var, command=self._on_toggles, bg=colors.bg_surface,
                fg=colors.text_primary, selectcolor=colors.bg_surface_hover, activebackground=colors.bg_surface,
                activeforeground=colors.text_primary, font=self._font,
            ).pack(side=tk.LEFT, padx=(0, spacing.xs))
        self._scale_names = (KEY_SCALE, *available_scales())
        self.scale_selector = ttk.Combobox(
            row2, state="readonly", width=20, font=self._font,
            values=tuple(t("keyboard.scale.project_key") if n == KEY_SCALE else t(f"keyboard.scale.{n}")
                         for n in self._scale_names),
        )
        self.scale_selector.current(0)
        self.scale_selector.pack(side=tk.LEFT, padx=spacing.xs)
        self.scale_selector.bind("<<ComboboxSelected>>", lambda _e: self._on_scale())
        key_card = theme.make_surface_card(container, radius=theme.corner_radius, padding=spacing.xs, auto_height=True)
        key_card.pack(fill=tk.X)
        self.keyboard = PianoKeyboardCanvas(
            key_card.inner, colors, self._font, on_press=self._on_key_press, on_release=self._on_key_release,
        )
        self.keyboard.pack(fill=tk.X)
        self.keyboard.bind("<KeyPress>", self._on_computer_key_press)
        self.keyboard.bind("<KeyRelease>", self._on_computer_key_release)
        self.keyboard.bind("<FocusOut>", self._on_focus_out)
        self.keyboard.bind("<Left>", lambda _e: self._shift(-12) or "break")
        self.keyboard.bind("<Right>", lambda _e: self._shift(12) or "break")
        self.keyboard.bind("<Prior>", lambda _e: self._step(-1) or "break")
        self.keyboard.bind("<Next>", lambda _e: self._step(1) or "break")
        range_row = tk.Frame(key_card.inner, bg=colors.bg_surface)
        range_row.pack(fill=tk.X, pady=(spacing.xs, 0))
        # Packed right-to-left so the row reads "Octave −  Fit  Octave +".
        self.octave_up_btn = create_button(range_row, text=t("keyboard.octave.up"),
                                           command=lambda: self._shift(12), bg=colors.bg_active,
                                           fg=colors.text_primary)
        self.octave_up_btn.pack(side=tk.RIGHT)
        self.fit_btn = create_button(range_row, text=t("keyboard.fit"), command=self._fit, bg=colors.bg_active,
                                     fg=colors.text_primary)
        self.fit_btn.pack(side=tk.RIGHT, padx=spacing.xs)
        self.octave_down_btn = create_button(range_row, text=t("keyboard.octave.down"),
                                             command=lambda: self._shift(-12), bg=colors.bg_active,
                                             fg=colors.text_primary)
        self.octave_down_btn.pack(side=tk.RIGHT)
        self.range_label = tk.Label(range_row, text="", bg=colors.bg_surface, fg=colors.text_secondary,
                                    font=self._font, anchor=tk.W)
        self.range_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        actions = tk.Frame(container, bg=colors.bg_window)
        actions.pack(fill=tk.X, pady=(spacing.sm, 0))
        self._action_frame = actions
        self.clear_btn = create_button(actions, text=t("keyboard.clear"), command=self._clear,
                                       bg=colors.bg_active, fg=colors.text_primary)
        self.candidate_selector = ttk.Combobox(actions, state="readonly", width=24, font=self._font)
        self.add_btn = create_button(actions, text=t("keyboard.add_to_progression"), command=self._add_candidate,
                                     bg=colors.harmonic_tonic, fg=colors.text_inverted)
        self.exercise_selector = ttk.Combobox(
            actions, state="readonly", width=34, font=self._font,
            values=tuple(t(e.prompt_key) for e in self.workbench.exercises),
        )
        self.exercise_selector.current(0)
        self.exercise_selector.bind("<<ComboboxSelected>>", lambda _e: self._on_exercise())
        self.check_btn = create_button(actions, text=t("keyboard.practice.check"), command=self._check,
                                       bg=colors.harmonic_tonic, fg=colors.text_inverted)
        self.solution_btn = create_button(actions, text=t("keyboard.practice.solution"), command=self._solution,
                                          bg=colors.bg_active, fg=colors.text_primary)
        self.next_exercise_btn = create_button(actions, text=t("keyboard.practice.next"),
                                               command=self._next_exercise, bg=colors.bg_active,
                                               fg=colors.text_primary)

        text_card = theme.make_surface_card(container, radius=theme.corner_radius, padding=spacing.xs)
        text_card.pack(fill=tk.BOTH, expand=True, pady=(spacing.sm, 0))
        self.info_text = tk.Text(
            text_card.inner, height=8, wrap=tk.WORD, state=tk.DISABLED, bg=colors.bg_surface,
            fg=colors.text_primary, font=self._font, relief=tk.FLAT, bd=0, padx=spacing.sm, pady=spacing.sm,
        )
        configure_readonly_preview(self.info_text, colors)
        scrollbar = ThemedAutoScrollbar(
            text_card.inner, bg_color=colors.bg_surface, track_color=colors.bg_surface_hover,
            thumb_color=colors.border, active_thumb_color=colors.harmonic_tonic, width=10, radius=5,
            orient="vertical",
        )
        scrollbar.set_command(self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        create_button(container, text=t("keyboard.close"), command=self._close, bg=colors.bg_active,
                      fg=colors.text_primary).pack(side=tk.BOTTOM, anchor=tk.E, pady=(spacing.sm, 0),
                                                   before=key_card)
        controller.add_listener(self._on_controller_change)
        self._layout_mode_controls()
        self.refresh()
        self._show(self.keyboard)

    # -- lifecycle ------------------------------------------------------------------
    def _close(self) -> None:
        self._controller.remove_listener(self._on_controller_change)
        self.workbench.input.release_all()
        super()._close()

    def _on_controller_change(self) -> None:
        if not self.window.winfo_exists():
            self._controller.remove_listener(self._on_controller_change)
            return
        self.refresh()

    # -- rendering --------------------------------------------------------------------
    def refresh(self) -> None:
        """Re-read the project and repaint; safe to call repeatedly (no event loops)."""
        if self._refreshing:
            return
        self._refreshing = True
        try:
            self._revision = self._controller.revision
            self.workbench.sync()
            self._update_events()
            model = self.workbench.view_model()
            self.keyboard.set_model(model)
            t = self._i18n.translate
            viewport = model.viewport
            self.range_label.configure(text=t(
                "keyboard.range", low=viewport.low, high=viewport.high,
                below=len(model.hidden_below), above=len(model.hidden_above),
            ))
            self._update_candidates()
            try:
                text = describe_workbench(self.workbench, t)
            except MusicTheoryError as exc:
                text = t("keyboard.info.error", error=exc)
            self._write_info(text)
        finally:
            self._refreshing = False

    def _write_info(self, text: str) -> None:
        self.info_text.configure(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert("1.0", text)
        self.info_text.configure(state=tk.DISABLED)

    def _update_events(self) -> None:
        chords = self._controller.session.chords
        values = tuple(
            self._i18n.translate("keyboard.event.label", number=i + 1, chord=chord) for i, chord in enumerate(chords)
        )
        self.event_selector.configure(values=values)
        if self.workbench.selected_index is not None and values:
            self.event_selector.current(self.workbench.selected_index)
        else:
            self.event_selector.set("")

    def _update_candidates(self) -> None:
        if self.workbench.mode is not KeyboardMode.FREE_INPUT:
            self._candidates = ()
            return
        result = self.workbench.recognition()
        self._candidates = tuple(c for c in result.candidates if c.kind is not CandidateKind.INCOMPLETE)
        values = tuple(c.symbol(self.workbench.convention) for c in self._candidates)
        current = self.candidate_selector.get()
        self.candidate_selector.configure(values=values)
        if values:
            self.candidate_selector.current(values.index(current) if current in values else 0)
        else:
            self.candidate_selector.set("")
        self.add_btn.configure(state=tk.NORMAL if values else tk.DISABLED)

    def _layout_mode_controls(self) -> None:
        for widget in self._action_frame.winfo_children():
            widget.pack_forget()
        mode = self.workbench.mode
        spacing = self._theme.spacing
        progression = mode is KeyboardMode.PROGRESSION
        for widget in (self.prev_btn, self.next_btn, self.rotate_down_btn, self.rotate_up_btn):
            widget.configure(state=tk.NORMAL if progression else tk.DISABLED)
        self.event_selector.configure(state="readonly" if progression else tk.DISABLED)
        self.voicing_selector.configure(state="readonly" if progression else tk.DISABLED)
        if mode is KeyboardMode.FREE_INPUT:
            self.clear_btn.pack(side=tk.LEFT)
            self.candidate_selector.pack(side=tk.LEFT, padx=spacing.xs)
            self.add_btn.pack(side=tk.LEFT)
        elif mode is KeyboardMode.PRACTICE:
            self.exercise_selector.pack(side=tk.LEFT)
            self.check_btn.pack(side=tk.LEFT, padx=spacing.xs)
            self.solution_btn.pack(side=tk.LEFT)
            self.next_exercise_btn.pack(side=tk.LEFT, padx=spacing.xs)
            self.clear_btn.pack(side=tk.LEFT)

    # -- controls ---------------------------------------------------------------------
    def _on_mode(self) -> None:
        self.workbench.mode = MODES[self.mode_selector.current()]
        self.workbench.input.release_all()
        self.workbench.feedback = None
        self._layout_mode_controls()
        self.refresh()

    def _on_event(self) -> None:
        index = self.event_selector.current()
        if index >= 0:
            self.workbench.select(index)
            self.refresh()

    def _step(self, delta: int) -> None:
        if self.workbench.mode is KeyboardMode.PROGRESSION:
            self.workbench.step(delta)
            self.refresh()

    def _on_voicing(self) -> None:
        self.workbench.set_voicing_type(VOICING_TYPES[self.voicing_selector.current()])
        self.refresh()

    def _rotate(self, delta: int) -> None:
        self.workbench.rotate(delta)
        self.refresh()

    def _on_toggles(self) -> None:
        wb = self.workbench
        wb.show_chord = self._vars["chord"].get()
        wb.show_scale = self._vars["scale"].get()
        wb.compare_previous = self._vars["compare"].get()
        wb.show_all_names = self._vars["names"].get()
        self.refresh()

    def _on_scale(self) -> None:
        self.workbench.scale_name = self._scale_names[self.scale_selector.current()]
        if not self._vars["scale"].get():
            self._vars["scale"].set(True)
            self.workbench.show_scale = True
        self.refresh()

    def _shift(self, semitones: int) -> None:
        self.workbench.auto_fit = False
        self.workbench.viewport = self.workbench.viewport.shifted(semitones)
        self.refresh()

    def _fit(self) -> None:
        self.workbench.auto_fit = True
        self.refresh()

    # -- note input -------------------------------------------------------------------
    def _latching(self) -> bool:
        return self.workbench.mode in (KeyboardMode.FREE_INPUT, KeyboardMode.PRACTICE)

    def _on_key_press(self, midi: int, source: InputSource = InputSource.MOUSE) -> None:
        if self.workbench.input.press(midi, source) and self._latching():
            self.workbench.input.toggle_selected(midi)
            self.workbench.feedback = None
        self.refresh()

    def _on_key_release(self, midi: int) -> None:
        self.workbench.input.release(midi)
        self.refresh()

    def computer_key_note(self, keysym: str) -> Optional[int]:
        name = _LAYOUT_ALIASES.get(keysym.lower(), keysym.lower())
        if name not in COMPUTER_KEYS:
            return None
        viewport = self.workbench.viewport
        base = viewport.low + (-viewport.low) % 12
        note = base + COMPUTER_KEYS.index(name)
        return note if viewport.contains(note) else None

    def _on_computer_key_press(self, event: tk.Event) -> Optional[str]:
        name = event.keysym.lower()
        if name in self._held_computer_keys:  # auto-repeat
            return "break"
        note = self.computer_key_note(name)
        if note is None:
            return None
        self._held_computer_keys[name] = note
        self._on_key_press(note, InputSource.COMPUTER_KEYBOARD)
        return "break"

    def _on_computer_key_release(self, event: tk.Event) -> Optional[str]:
        # Release the note this key pressed, even if the viewport moved meanwhile.
        note = self._held_computer_keys.pop(event.keysym.lower(), None)
        if note is None:
            return None
        self._on_key_release(note)
        return "break"

    def _on_focus_out(self, _event: tk.Event) -> None:
        self._held_computer_keys.clear()
        if self.workbench.input.release_all():
            self.refresh()

    def _clear(self) -> None:
        self.workbench.input.clear_selected()
        self.workbench.input.release_all()
        self.workbench.feedback = None
        self.workbench.show_practice_solution = False
        self.refresh()

    # -- project change (undoable) ---------------------------------------------------------
    def _add_candidate(self) -> None:
        index = self.candidate_selector.current()
        if not 0 <= index < len(self._candidates):
            return
        try:
            symbol = self.workbench.project_symbol_for(self._candidates[index])
            self._controller.add_chord(symbol)
        except (MusicTheoryError, ValueError) as exc:
            self._write_info(self._i18n.translate("keyboard.add_error", error=exc))
            return
        new_index = len(self._controller.session.chords) - 1
        self.workbench.select(new_index)
        self._on_project_change(new_index)
        self.refresh()

    # -- practice ---------------------------------------------------------------------------
    def _on_exercise(self) -> None:
        self.workbench.select_exercise(self.exercise_selector.current())
        self.refresh()

    def _check(self) -> None:
        self.workbench.check_practice()
        self.refresh()

    def _solution(self) -> None:
        self.workbench.show_practice_solution = True
        self.refresh()

    def _next_exercise(self) -> None:
        index = (self.workbench.exercise_index + 1) % len(self.workbench.exercises)
        self.exercise_selector.current(index)
        self._on_exercise()


__all__ = ["COMPUTER_KEYS", "KeyboardDialog", "describe_workbench"]
