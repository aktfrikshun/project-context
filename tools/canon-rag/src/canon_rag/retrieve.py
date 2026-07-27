from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from .authority import AUTHORITY_SCORE
from .embeddings import EmbeddingAdapter, HashEmbeddingAdapter, cosine, tokens


@dataclass(frozen=True)
class SearchOptions:
    limit: int = 10
    include_deprecated: bool = False
    include_generated: bool = False
    include_historical: bool = False
    statuses: tuple[str, ...] = ()
    authorities: tuple[str, ...] = ()


def _eligible(record: dict[str, object], options: SearchOptions) -> bool:
    authority = str(record.get("authority", "current_guidance"))
    if authority == "deprecated" and not options.include_deprecated:
        return False
    if authority == "generated_artifact" and not options.include_generated:
        return False
    if authority == "historical" and not options.include_historical:
        return False
    if not bool(record.get("default_eligible", True)) and authority not in {
        "deprecated" if options.include_deprecated else "",
        "generated_artifact" if options.include_generated else "",
        "historical" if options.include_historical else "",
    }:
        return False
    if options.statuses and str(record.get("status")) not in options.statuses:
        return False
    if options.authorities and authority not in options.authorities:
        return False
    return True


def _bm25(records: list[dict[str, object]], query_terms: list[str]) -> list[float]:
    documents = [tokens(f"{record.get('title', '')} {record.get('heading', '')} {record.get('text', '')}") for record in records]
    if not documents or not query_terms:
        return [0.0] * len(records)
    average_length = sum(map(len, documents)) / len(documents) or 1.0
    frequencies = [Counter(document) for document in documents]
    document_frequency = Counter(term for term in set(query_terms) for document in documents if term in document)
    scores: list[float] = []
    for document, frequency in zip(documents, frequencies):
        score = 0.0
        for term in query_terms:
            tf = frequency[term]
            if not tf:
                continue
            df = document_frequency[term]
            inverse = math.log(1 + (len(documents) - df + 0.5) / (df + 0.5))
            denominator = tf + 1.2 * (1 - 0.75 + 0.75 * len(document) / average_length)
            score += inverse * tf * 2.2 / denominator
        scores.append(score)
    maximum = max(scores, default=0.0) or 1.0
    return [score / maximum for score in scores]


def search(
    records: Iterable[dict[str, object]],
    query: str,
    options: SearchOptions | None = None,
    embedder: EmbeddingAdapter | None = None,
) -> list[dict[str, object]]:
    options = options or SearchOptions()
    embedder = embedder or HashEmbeddingAdapter()
    cyber_terms = (
        "cybernetic", "artificial eye", "synthetic skin", "fiber optic",
        "fiber-optic", "prosthetic", "which side",
    )
    cyber_query = any(term in query.casefold() for term in cyber_terms)
    candidates = [
        record
        for record in records
        if _eligible(record, options)
        and (
            cyber_query
            or "cybernetic-chloe" not in str(record.get("path", ""))
            and not str(record.get("path", "")).endswith("experience/cybernetic-body.md")
        )
    ]
    lexical = _bm25(candidates, tokens(query))
    query_vector = embedder.embed(query)
    scored: list[dict[str, object]] = []
    for record, lexical_score in zip(candidates, lexical):
        vector = record.get("embedding")
        semantic_score = max(0.0, cosine(query_vector, vector if isinstance(vector, list) else embedder.embed(str(record.get("text", "")))))
        authority = str(record.get("authority", "current_guidance"))
        authority_score = int(record.get("authority_score", AUTHORITY_SCORE.get(authority, 0))) / 600
        exact_anatomy = sum(
            phrase in query.casefold() and phrase in str(record.get("text", "")).casefold()
            for phrase in ("left arm", "left leg", "artificial eye", "right arm", "right leg")
        )
        path = str(record.get("path", ""))
        continuity_bonus = 0.0
        if cyber_query and (path.endswith("experience/cybernetic-body.md") or path.endswith("assets/cybernetic-chloe-v1/MODEL_CARD.md")):
            continuity_bonus = 0.90
        elif cyber_query and path.endswith("assets/chloe-model-v1/MODEL_CARD.md"):
            continuity_bonus = 0.75
        elif not cyber_query and any(term in query.casefold() for term in ("ordinary chloe", "generate", "appearance", "visual")) and path.endswith("assets/chloe-model-v1/MODEL_CARD.md"):
            continuity_bonus = 0.35
        final = 0.55 * lexical_score + 0.25 * semantic_score + 0.20 * authority_score + 0.10 * exact_anatomy + continuity_bonus
        result = dict(record)
        result["scores"] = {
            "lexical": round(lexical_score, 6),
            "semantic": round(semantic_score, 6),
            "authority": round(authority_score, 6),
            "exact_anatomy": exact_anatomy,
            "continuity": continuity_bonus,
        }
        result["final_score"] = round(final, 6)
        result.pop("embedding", None)
        scored.append(result)
    scored.sort(key=lambda item: (-float(item["final_score"]), str(item.get("path")), str(item.get("id"))))
    return scored[: options.limit]
