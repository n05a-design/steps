"""
STEPS Architecture Ports: Knowledge Lookup Port.

Adheres to:
- ADR-008 (KI-Skill & Knowledge Base)
- Prompt 07, Prompt 15
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol


class KnowledgeLookupPort(Protocol):
    """Protocol for accessing grounded musical knowledge without LLM hallucinations."""

    def get_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves verified bibliographic source metadata."""
        ...

    def get_concept(self, concept_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves structured musical concept definition and relations."""
        ...

    def query_claims(self, query: str, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """Searches claims matching query keywords within an optional musical domain."""
        ...

    def get_reviewed_progression(self, prog_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves reviewed progression example with source citations."""
        ...
