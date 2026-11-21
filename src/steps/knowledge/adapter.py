"""Look up approved STEPS pilot claims with precise sources and note spelling."""

from __future__ import annotations

from dataclasses import dataclass, replace
import logging
from pathlib import Path
import re
from typing import Literal
from unicodedata import normalize

from ..progression import reviewed
from ..theory.pitch import parse_spelling

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[3]
PRODUCT_REGISTRY_PATH = reviewed.REGISTRY
HISTORIC_REGISTRY_PATH = ROOT / "knowledge/sources/curated_sources_registry.yaml"
REVIEWED_PROGRESSIONS_PATH = reviewed.CATALOG

_ALIASES = {
    "PROG-001": ("four chords", "axis"),
    "PROG-003": ("ii-v-i", "2-5-1", "two-five-one"),
    "PROG-009": ("minor plagal", "minor plagal cadence", "mollsubdominante"),
}
_NOTE_QUESTION = re.compile(
    r"welcher ton ist ['\"]?b['\"]? im (?:deutschen|internationalen) sprachraum"
)
_AMBIGUOUS_B = re.compile(
    r"(?:b|erkläre den akkord ['\"]?b['\"]? ohne angabe der notationskonvention)"
)
_RESTRICTED = re.compile(
    r"\b(?:z-library|pirated|volltext kopieren)\b"
    r"|\b(?:volltext|buchscans?)\b.*\b(?:repository|bundle|ausliefern|verbreiten)\b"
    r"|\bglide\b.*\bohne lizenzübernahme\b"
)


@dataclass(frozen=True)
class KnowledgeSource:
    """Bibliographic source entry."""

    source_id: str
    title: str
    authors: tuple[str, ...]
    url: str
    rights_status: str
    locator: str = ""
    is_product_source: bool = False


@dataclass(frozen=True)
class KnowledgeClaim:
    """An individual atomic claim with precise source attribution."""

    claim_id: str
    summary: str
    kind: str
    citation: KnowledgeSource
    verified: bool = False
    alternative_interpretations: tuple[str, ...] = ()
    citations: tuple[KnowledgeSource, ...] = ()


@dataclass(frozen=True)
class QueryResult:
    """Result of a query against the grounded knowledge base."""

    found: bool
    status: Literal[
        "GROUNDED", "ALTERNATIVE_INTERPRETATIONS", "NO_EVIDENCE",
        "RESTRICTED_LOCAL", "AMBIGUOUS_REJECTION",
    ]
    query: str
    claims: tuple[KnowledgeClaim, ...] = ()
    explanation: str = ""
    sources: tuple[KnowledgeSource, ...] = ()
    alternatives: tuple[str, ...] = ()


def _query_key(text: str) -> str:
    value = normalize("NFKC", text).casefold()
    value = value.translate(str.maketrans({"–": "-", "—": "-", "−": "-", "’": "'", "‘": "'"}))
    value = re.sub(r"\s*-\s*", "-", value)
    return " ".join(value.split()).rstrip("?.!")


def _international_text(claim: reviewed.Claim) -> str:
    # The reviewed voice paths identify the German note tokens in these statements.
    # Never rewrite citation text, free-form words or the notation-comparison claim.
    names = {}
    for _, written in claim.voice_path:
        note = parse_spelling(written, "DE")
        names[note.render("DE").removesuffix(str(note.octave))] = (
            note.render("INT").removesuffix(str(note.octave))
        )
    if not names:
        return claim.text
    tokens = "|".join(re.escape(name) for name in sorted(names, key=len, reverse=True))
    return re.sub(rf"(?<![\w♭♯#])(?:{tokens})(?![\w♭♯#])", lambda match: names[match[0]], claim.text)


class KnowledgeAdapter:
    """Retrieve approved pilot claims by explicit concept, sequence or claim ID."""

    def __init__(self, product_registry: Path | None = None, reviewed_progressions: Path | None = None):
        self._sources: dict[str, KnowledgeSource] = {}
        self._claims: dict[str, KnowledgeClaim] = {}
        self._international: dict[str, str] = {}
        self._concept_index: dict[str, tuple[str, ...]] = {}
        self._load_data(
            product_registry or PRODUCT_REGISTRY_PATH, reviewed_progressions or REVIEWED_PROGRESSIONS_PATH,
        )

    def _load_data(self, registry_path: Path, catalog_path: Path) -> None:
        try:
            registry = reviewed._sources(registry_path)
            sources = {}
            for ident, entry in registry.items():
                authors = entry.get("authors", [])
                if not isinstance(authors, list) or any(not isinstance(author, str) for author in authors):
                    raise reviewed.PublicationError(f"{ident}: invalid author metadata.")
                sources[ident] = KnowledgeSource(
                    ident, entry.get("title", ""), tuple(authors),
                    entry.get("url", ""), entry.get("rights_status", ""), is_product_source=True,
                )
            self._sources = sources
            catalog = reviewed._load_reviewed_catalog(registry, catalog_path)
        except reviewed.PublicationError as exc:
            logger.warning("Knowledge pilot unavailable: %s", exc)
            return

        claims = {}
        international = {}
        index = {}
        for example in catalog:
            progression = example.progression
            ids = tuple(entry.claim.claim_id for entry in example.claims[1:])
            for key in (progression.prog_id, progression.name, progression.roman_numerals,
                        progression.chords_str, *_ALIASES.get(progression.prog_id, ())):
                index[_query_key(key)] = ids
            for entry in example.claims:
                claim = entry.claim
                if claim.claim_id in claims:
                    continue
                citations = tuple(
                    replace(self._sources[ref.source_id], locator=ref.locator) for ref in claim.citations
                )
                claims[claim.claim_id] = KnowledgeClaim(
                    claim.claim_id, claim.text, claim.kind, citations[0],
                    verified=True, citations=citations,
                )
                international[claim.claim_id] = _international_text(claim)
                index[_query_key(claim.claim_id)] = (claim.claim_id,)
        for key in ("notation", "int/de", "de/int"):
            index[key] = (reviewed.NOTATION,)
        self._claims, self._international, self._concept_index = claims, international, index

    def get_source(self, source_id: str) -> KnowledgeSource | None:
        """Resolve registered source metadata."""
        return self._sources.get(source_id)

    def get_claim(self, claim_id: str) -> KnowledgeClaim | None:
        """Resolve an approved claim by ID in its reviewed wording."""
        return self._claims.get(claim_id)

    def query(self, query_text: str, convention: Literal["INT", "DE"] | None = None) -> QueryResult:
        """Return an exact pilot match, a notation clarification or the absence of evidence."""
        if convention not in (None, "INT", "DE"):
            raise ValueError("Notation convention must be INT or DE.")
        key = _query_key(query_text)
        if _RESTRICTED.search(key):
            return QueryResult(
                False, "RESTRICTED_LOCAL", query_text,
                explanation="Für fremde Volltexte (Klasse E) und ohne Nutzungserlaubnis übernommene Dateien "
                            "sieht STEPS keine Freigabe vor.",
            )

        if _AMBIGUOUS_B.fullmatch(key):
            if convention is None:
                return QueryResult(
                    False, "AMBIGUOUS_REJECTION", query_text,
                    explanation="Bitte gib die Schreibkonvention INT oder DE für B an.",
                )
            key = "notation"
        elif _NOTE_QUESTION.fullmatch(key):
            key = "notation"

        ids = self._concept_index.get(key, ())
        if ids:
            claims = tuple(
                replace(self._claims[ident], summary=self._international[ident])
                if convention != "DE" else self._claims[ident]
                for ident in ids
            )
            sources = tuple(dict.fromkeys(source for claim in claims for source in claim.citations))
            return QueryResult(
                True, "GROUNDED", query_text, claims=claims,
                explanation=" ".join(claim.summary for claim in claims), sources=sources,
            )
        return QueryResult(
            False, "NO_EVIDENCE", query_text,
            explanation=f"Für die Anfrage {query_text!r} liegt kein geprüfter Primärbeleg in der STEPS-Wissensbasis vor.",
        )
