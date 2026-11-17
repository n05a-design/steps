"""STEPS Knowledge Adapter subsystem: Grounded knowledge retrieval and evidence verification."""
from __future__ import annotations

from .adapter import KnowledgeAdapter, KnowledgeClaim, KnowledgeSource, QueryResult

__all__ = [
    "KnowledgeAdapter",
    "KnowledgeSource",
    "KnowledgeClaim",
    "QueryResult",
]
