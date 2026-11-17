"""
STEPS Storage Core: Undo/Redo History Stack & Dirty State Tracking.

Adheres to:
- M07 (Transaktionssicherheit & Undo/Redo)
- Zero data loss, bounded memory footprint
- Clean/dirty state tracking synchronized with file save operations
"""

from __future__ import annotations

import copy
from typing import Generic, List, Optional, TypeVar

from .exceptions import UndoRedoError

T = TypeVar("T")


class UndoStack(Generic[T]):
    """
    Generic Undo/Redo stack with bounded history depth and save-point tracking.
    """
    def __init__(self, initial_state: T, max_depth: int = 50):
        if max_depth < 1:
            raise ValueError(f"max_depth must be >= 1, got {max_depth}")
        self.max_depth = max_depth
        self._history: List[T] = [copy.deepcopy(initial_state)]
        self._current_index: int = 0
        self._clean_index: Optional[int] = 0

    @property
    def current_state(self) -> T:
        """Returns the current active state."""
        return self._history[self._current_index]

    @property
    def can_undo(self) -> bool:
        """Returns True if there is a previous state to revert to."""
        return self._current_index > 0

    @property
    def can_redo(self) -> bool:
        """Returns True if there is a forward state to advance to."""
        return self._current_index < len(self._history) - 1

    @property
    def is_dirty(self) -> bool:
        """Returns True if the current state differs from the last saved state."""
        return self._current_index != self._clean_index

    def push(self, new_state: T) -> None:
        """
        Pushes a new state onto the history stack.
        Discards any forward redo history past current index.
        Truncates oldest entries if exceeding max_depth.
        """
        # Truncate forward history
        self._history = self._history[:self._current_index + 1]
        
        # If clean index was in discarded forward history, it becomes unreachable
        if self._clean_index is not None and self._clean_index > self._current_index:
            self._clean_index = None

        self._history.append(copy.deepcopy(new_state))
        self._current_index += 1

        # Enforce max depth
        if len(self._history) > self.max_depth:
            overflow = len(self._history) - self.max_depth
            self._history = self._history[overflow:]
            self._current_index -= overflow
            if self._clean_index is not None:
                self._clean_index -= overflow
                if self._clean_index < 0:
                    self._clean_index = None

    def undo(self) -> T:
        """Reverts to the previous state. Raises UndoRedoError if at bottom of stack."""
        if not self.can_undo:
            raise UndoRedoError("Cannot undo: already at the earliest state.")
        self._current_index -= 1
        return self.current_state

    def redo(self) -> T:
        """Advances to the next forward state. Raises UndoRedoError if at top of stack."""
        if not self.can_redo:
            raise UndoRedoError("Cannot redo: already at the latest state.")
        self._current_index += 1
        return self.current_state

    def mark_clean(self) -> None:
        """Marks the current state as the saved/clean state."""
        self._clean_index = self._current_index
