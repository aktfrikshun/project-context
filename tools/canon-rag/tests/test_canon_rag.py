from __future__ import annotations

import json
from pathlib import Path

from canon_rag.authority import classify
from canon_rag.build import build_baseline, build_chunks, discover
from canon_rag.markdown import load_document, sections
from canon_rag.validate import validate

ROOT = Path(__file__).resolve().parents[3]


def test_required_files_are_discovered() -> None:
    paths = {path.relative_to(ROOT).as_posix() for path in discover(ROOT)}
    assert "projects/chloekatastrophe/overview.md" in paths
    assert "projects/chloekatastrophe/AI_CONTEXT.md" in paths
    assert not any(path.endswith("_prompt_audit.md") for path in paths)


def test_chunks_are_stable_and_source_addressed() -> None:
    first = build_chunks(ROOT, "abc123")
    second = build_chunks(ROOT, "abc123")
    assert first == second
    assert len({chunk["id"] for chunk in first}) == len(first)
    assert all(chunk["source_revision"] == "abc123" for chunk in first)
    json.dumps(first)


def test_baseline_preserves_required_sources() -> None:
    baseline = build_baseline(ROOT, "abc123")
    assert "projects/chloekatastrophe/overview.md" in baseline
    assert "projects/chloekatastrophe/AI_CONTEXT.md" in baseline
    assert "Source revision: `abc123`" in baseline


def test_deprecated_content_is_not_default_eligible() -> None:
    path = ROOT / "projects/chloekatastrophe/history/deprecated.md"
    document = load_document(ROOT, path)
    result = classify(document, sections(document)[0])
    assert result["authority"] == "deprecated"
    assert result["default_eligible"] is False


def test_active_model_card_is_accepted_visual_canon() -> None:
    path = ROOT / "projects/chloekatastrophe/assets/chloe-model-v1/MODEL_CARD.md"
    document = load_document(ROOT, path)
    result = classify(document, sections(document)[0])
    assert result["authority"] == "accepted_canon"
    assert result["default_eligible"] is True


def test_cybernetic_specification_is_accepted_visual_canon() -> None:
    path = ROOT / "projects/chloekatastrophe/experience/cybernetic-body.md"
    document = load_document(ROOT, path)
    result = classify(document, sections(document)[0])
    assert result["authority"] == "accepted_canon"
    assert result["requires_status_label"] is False


def test_section_status_overrides_document_authority() -> None:
    path = ROOT / "projects/chloekatastrophe/experience/cybernetic-body.md"
    document = load_document(ROOT, path)
    classified = {section.heading: classify(document, section) for section in sections(document)}
    assert classified["Accepted visual design"]["authority"] == "accepted_canon"
    assert classified["Implementation and generation guidance"]["authority"] == "implementation_detail"
    assert classified["Unresolved questions"]["authority"] == "unresolved"
    assert classified["Deprecated concepts"]["authority"] == "deprecated"
    assert classified["Deprecated concepts"]["default_eligible"] is False


def test_artificial_left_eye_decision_is_accepted() -> None:
    path = ROOT / "projects/chloekatastrophe/decisions/adr-006-cybernetic-left-eye.md"
    document = load_document(ROOT, path)
    result = classify(document, sections(document)[0])
    assert result["authority"] == "accepted_decision"
    assert result["default_eligible"] is True


def test_repository_validates() -> None:
    assert validate(ROOT) == []
