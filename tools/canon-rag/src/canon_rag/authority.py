from __future__ import annotations

import re

from .model import Document, Section

AUTHORITY_SCORE = {
    "accepted_canon": 600,
    "accepted_decision": 550,
    "current_guidance": 500,
    "implementation_detail": 400,
    "draft_canon": 300,
    "proposal": 250,
    "unresolved": 200,
    "generated_artifact": 150,
    "historical": 100,
    "deprecated": 0,
}

STATUS_PATTERN = re.compile(
    r"(?:\*\*)?status(?:\*\*)?\s*:\s*([^\n]+)", re.IGNORECASE
)


def _normalized_status(document: Document, section: Section) -> str:
    explicit = str(document.metadata.get("status", "")).lower()
    explicit_authority = str(document.metadata.get("authority", "")).lower()
    status_match = STATUS_PATTERN.search(section.body)
    section_status = status_match.group(1).lower() if status_match else ""
    status = f"{explicit} {section_status} {section.heading.lower()}"
    path = document.path.lower()

    if explicit_authority in AUTHORITY_SCORE:
        return explicit_authority
    if "/assets/chloe-model-v1/" in path and path.endswith(("model_card.md", "readme.md")):
        return "accepted_canon"
    if "deprecated" in path or any(word in status for word in ("deprecated", "superseded", "rejected")):
        return "deprecated"
    if "unresolved" in path or any(word in status for word in ("unresolved", "open question", "contradiction")):
        return "unresolved"
    if "intake_pending" in status or "intake pending" in status:
        return "unresolved"
    if any(word in status for word in ("draft canon", "draft approved")):
        return "draft_canon"
    if any(word in status for word in ("proposal", "proposed", "planned", "experimental")):
        return "proposal"
    if any(word in status for word in ("generated artifact", "generated work")):
        return "generated_artifact"
    if "/decisions/" in path and any(word in status for word in ("accepted", "complete")):
        return "accepted_decision"
    if any(word in status for word in ("accepted canon", "confirmed canon", "approved production visual canon")):
        return "accepted_canon"
    if "/history/" in path or "/provenance/" in path:
        return "historical"
    if "/projects/" in path or "/architecture/" in path or "/product/" in path:
        return "implementation_detail"
    return "current_guidance"


def classify(document: Document, section: Section) -> dict[str, object]:
    authority = _normalized_status(document, section)
    default_eligible = authority not in {"deprecated", "generated_artifact", "historical"}
    return {
        "authority": authority,
        "authority_score": AUTHORITY_SCORE[authority],
        "status": authority,
        "default_eligible": default_eligible,
        "requires_status_label": authority
        in {"draft_canon", "proposal", "unresolved", "generated_artifact", "historical", "deprecated"},
    }
