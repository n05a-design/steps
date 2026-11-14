"""Access to individually reviewed learning examples for the desktop app."""

from pathlib import Path

from src.steps.progression.engine import ReviewedProgression
from src.steps.progression.reviewed import PublicationError, load_reviewed_catalog

__all__ = ["get_reviewed_progression", "list_reviewed_progressions"]

REGISTRY = Path(__file__).resolve().parents[1] / "knowledge/sources/registry.yaml"


def list_reviewed_progressions() -> tuple[ReviewedProgression, ...]:
    """Load the app's pilot examples using its product source register."""
    return load_reviewed_catalog(registry_path=REGISTRY)


def get_reviewed_progression(prog_id: str) -> ReviewedProgression:
    """Return a published pilot example by its identifier."""
    for example in list_reviewed_progressions():
        if example.progression.prog_id == prog_id:
            return example
    raise PublicationError(f"Progression {prog_id!r} is outside the reviewed pilot.")
