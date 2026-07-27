from __future__ import annotations

import json
from pathlib import Path

from .build import PROJECT, revision
from .retrieve import SearchOptions, search
from .storage import FileIndexStore


class CanonService:
    def __init__(self, repository: Path, index_root: Path):
        self.repository = repository.resolve()
        self.store = FileIndexStore(index_root.resolve())

    def _release(self) -> tuple[str, Path]:
        indexed = self.store.current_revision()
        if not indexed:
            raise RuntimeError("no published canon index")
        release = self.store.release_path(indexed)
        if not release.is_dir():
            raise RuntimeError(f"published index release is missing: {indexed}")
        return indexed, release

    def _records(self) -> tuple[str, list[dict[str, object]]]:
        indexed, release = self._release()
        with (release / "chunks.jsonl").open(encoding="utf-8") as stream:
            return indexed, [json.loads(line) for line in stream]

    def revision_info(self) -> dict[str, object]:
        indexed, _ = self._release()
        source = revision(self.repository)
        return {"project": "chloekatastrophe", "source_revision": source, "index_revision": indexed, "stale": indexed != source}

    def load_project_context(self, project: str) -> dict[str, object]:
        self._require_project(project)
        indexed, release = self._release()
        return {"project": project, "source_revision": indexed, "baseline": (release / "baseline.md").read_text(encoding="utf-8"), "revision": self.revision_info()}

    def search_knowledge(self, project: str, query: str, filters: dict[str, object] | None = None) -> dict[str, object]:
        self._require_project(project)
        indexed, records = self._records()
        filters = filters or {}
        options = SearchOptions(
            limit=int(filters.get("limit", 10)),
            include_deprecated=bool(filters.get("include_deprecated", False)),
            include_generated=bool(filters.get("include_generated", False)),
            include_historical=bool(filters.get("include_historical", False)),
            statuses=tuple(map(str, filters.get("statuses", []))),
            authorities=tuple(map(str, filters.get("authorities", []))),
        )
        return {"project": project, "query": query, "source_revision": indexed, "revision": self.revision_info(), "results": search(records, query, options)}

    def explain_retrieval(self, project: str, query: str) -> dict[str, object]:
        result = self.search_knowledge(project, query, {"limit": 10})
        result["policy"] = {
            "weights": {"lexical": 0.55, "semantic": 0.25, "authority": 0.20, "exact_anatomy_bonus": 0.10},
            "default_exclusions": ["deprecated", "generated_artifact", "historical"],
            "unresolved_status_preserved": True,
            "embedding_fallback": "hash-v1",
        }
        return result

    def get_source(self, project: str, path: str, commit_sha: str) -> dict[str, object]:
        self._require_project(project)
        if commit_sha != revision(self.repository):
            raise RuntimeError("requested commit does not match the checked-out published canon revision")
        candidate = (self.repository / path).resolve()
        candidate.relative_to(self.repository)
        if not candidate.is_file() or not candidate.is_relative_to(self.repository / PROJECT):
            raise FileNotFoundError(path)
        return {"project": project, "path": path, "source_revision": commit_sha, "text": candidate.read_text(encoding="utf-8")}

    def get_asset(self, project: str, asset_id: str, commit_sha: str) -> dict[str, object]:
        self._require_project(project)
        indexed, records = self._records()
        if commit_sha != indexed:
            raise RuntimeError("requested commit does not match the indexed canon revision")
        matches = [record for record in records if record.get("record_type") == "asset" and record.get("asset_id") == asset_id]
        if not matches:
            raise FileNotFoundError(asset_id)
        return matches[0]

    def health(self) -> dict[str, object]:
        return {"status": "ok"}

    def readiness(self) -> dict[str, object]:
        try:
            info = self.revision_info()
            return {"status": "ready" if not info["stale"] else "stale", **info}
        except RuntimeError as error:
            return {"status": "not_ready", "error": str(error)}

    @staticmethod
    def _require_project(project: str) -> None:
        if project != "chloekatastrophe":
            raise ValueError(f"unsupported project: {project}")
