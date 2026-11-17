"""
STEPS Architecture Ports: Events, Commands & Decoupled Bus.

Adheres to:
- REQ-019 (Engine von GUI trennen)
- ADR-007, Prompt 07 (Architektur, Events, Prozesse und Datenhaltung entkoppeln)
- Thread-safe publish-subscribe and command dispatching.
"""

from __future__ import annotations

import logging
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DomainEvent:
    """Immutable domain event representing something that occurred in the model."""
    name: str
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(frozen=True)
class Command:
    """User or system action requesting a state transition."""
    name: str
    params: Dict[str, Any] = field(default_factory=dict)
    source: str = "ui"


class EventBus:
    """Thread-safe event bus for publishing domain events to decoupled subscribers."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._subscribers: Dict[str, List[Callable[[DomainEvent], None]]] = {}

    def subscribe(self, event_name: str, callback: Callable[[DomainEvent], None]) -> None:
        """Subscribes a callback to a specific event name or '*' for all events."""
        with self._lock:
            if event_name not in self._subscribers:
                self._subscribers[event_name] = []
            if callback not in self._subscribers[event_name]:
                self._subscribers[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable[[DomainEvent], None]) -> None:
        """Removes a previously registered subscriber."""
        with self._lock:
            if event_name in self._subscribers and callback in self._subscribers[event_name]:
                self._subscribers[event_name].remove(callback)

    def publish(self, event: DomainEvent) -> None:
        """Publishes an event to matching subscribers."""
        with self._lock:
            callbacks = list(self._subscribers.get(event.name, []))
            wildcards = list(self._subscribers.get("*", []))

        # Invoke callbacks outside lock to avoid deadlocks
        for cb in callbacks + wildcards:
            try:
                cb(event)
            except Exception as e:
                logger.error("Error in EventBus subscriber %r for event %s: %s", cb, event.name, e)


class CommandRegistry:
    """Registry mapping command names to handlers."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._handlers: Dict[str, Callable[[Command], Any]] = {}

    def register(self, command_name: str, handler: Callable[[Command], Any]) -> None:
        with self._lock:
            self._handlers[command_name] = handler

    def execute(self, command: Command) -> Any:
        with self._lock:
            handler = self._handlers.get(command.name)
        if not handler:
            raise KeyError(f"No handler registered for command: {command.name}")
        return handler(command)

    def list_commands(self) -> List[str]:
        with self._lock:
            return sorted(list(self._handlers.keys()))
