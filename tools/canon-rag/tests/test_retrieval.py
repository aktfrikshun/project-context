from __future__ import annotations

import json
from pathlib import Path

from canon_rag.build import write_artifacts
from canon_rag.mcp_server import call, tool_definitions
from canon_rag.retrieve import SearchOptions, search
from canon_rag.service import CanonService
from canon_rag.storage import FileIndexStore

ROOT = Path(__file__).resolve().parents[3]
EVALUATION = ROOT / "tools/canon-rag/evaluation/chloekatastrophe.json"


def records() -> list[dict[str, object]]:
    return write_records("evaluation")


def write_records(revision: str) -> list[dict[str, object]]:
    from canon_rag.build import build_chunks
    from canon_rag.embeddings import HashEmbeddingAdapter

    embedder = HashEmbeddingAdapter()
    output = build_chunks(ROOT, revision)
    for record in output:
        record["embedding"] = embedder.embed(str(record["text"]))
    return output


def test_evaluation_contract() -> None:
    corpus = records()
    evaluation = json.loads(EVALUATION.read_text(encoding="utf-8"))
    for case in evaluation["cases"]:
        results = search(corpus, case["query"], SearchOptions(limit=20))
        paths = [str(result["path"]) for result in results]
        joined = "\n".join(str(result["text"]) for result in results)
        statuses = {str(result["status"]) for result in results}
        for required in case.get("required_paths", []):
            assert required in paths, (case["query"], required, paths)
        for prohibited in case.get("prohibited_paths", []):
            assert prohibited not in paths
        for fragment in case.get("prohibited_path_fragments", []):
            assert not any(fragment in path for path in paths)
        for text in case.get("required_text", []):
            assert text.casefold() in joined.casefold()
        for status in case.get("required_statuses", []):
            assert status in statuses


def test_exact_anatomy_beats_generic_cyberpunk_similarity() -> None:
    corpus = records()
    corpus.append({
        "id": "generic-cyberpunk",
        "path": "generic-cyberpunk.md",
        "title": "Generic cyberpunk",
        "heading": "Left arm",
        "text": "A cybernetic left arm with glowing chrome circuitry.",
        "authority": "current_guidance",
        "authority_score": 500,
        "status": "current_guidance",
        "default_eligible": True,
    })
    results = search(corpus, "Which side is Chloe's cybernetic left arm?", SearchOptions(limit=100))
    specification = [result for result in results if str(result["path"]).endswith("experience/cybernetic-body.md")]
    generic = next(result for result in results if result["id"] == "generic-cyberpunk")
    assert specification
    assert results.index(specification[0]) < 5
    assert specification[0]["final_score"] > generic["final_score"]


def test_generated_and_deprecated_require_explicit_filters() -> None:
    corpus = records()
    normal = search(corpus, "emerald eyes porcelain skin", SearchOptions(limit=50))
    assert all(result["authority"] not in {"deprecated", "generated_artifact"} for result in normal)
    historical = search(corpus, "emerald eyes porcelain skin", SearchOptions(limit=50, include_deprecated=True))
    assert any(result["authority"] == "deprecated" for result in historical)


def test_asset_records_have_checksum_id_path_and_revision() -> None:
    assets = [record for record in records() if record["record_type"] == "asset"]
    assert assets
    assert all(record.get("asset_id") and record.get("source_sha256") and record.get("path") for record in assets)
    assert all(record["source_revision"] == "evaluation" for record in assets)


def test_atomic_publish_incremental_reuse_and_service(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("CANON_SOURCE_REVISION", "revision-one")
    store = FileIndexStore(tmp_path / "index")
    first_stage = store.stage()
    first = write_artifacts(ROOT, first_stage)
    first_release = store.publish(first_stage, "revision-one")
    monkeypatch.setenv("CANON_SOURCE_REVISION", "revision-two")
    second_stage = store.stage()
    second = write_artifacts(ROOT, second_stage, previous_chunks=first_release / "chunks.jsonl")
    store.publish(second_stage, "revision-two")
    assert second["reused_embedding_count"] == second["chunk_count"]
    service = CanonService(ROOT, tmp_path / "index")
    assert service.load_project_context("chloekatastrophe")["source_revision"] == "revision-two"
    assert service.search_knowledge("chloekatastrophe", "Echo Traversal", {"limit": 2})["results"]
    assert service.readiness()["status"] == "ready"
    monkeypatch.setenv("CANON_SOURCE_REVISION", "revision-three")
    assert service.readiness()["status"] == "stale"
    assert store.rollback() == "revision-one"


def test_mcp_surface_is_stable(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("CANON_SOURCE_REVISION", "mcp-revision")
    store = FileIndexStore(tmp_path / "index")
    stage = store.stage()
    write_artifacts(ROOT, stage)
    store.publish(stage, "mcp-revision")
    service = CanonService(ROOT, tmp_path / "index")
    assert {tool["name"] for tool in tool_definitions()} == {
        "load_project_context", "search_knowledge", "get_source", "get_asset", "get_canon_revision", "explain_retrieval"
    }
    response = call(service, "explain_retrieval", {"project": "chloekatastrophe", "query": "Cybernetic Chloe"})
    assert response["results"]
    assert "policy" in response
