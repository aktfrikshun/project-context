from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path


class FileIndexStore:
    """Replaceable atomic filesystem adapter with one previous-good release."""

    def __init__(self, root: Path):
        self.root = root
        self.releases = root / "releases"
        self.current_file = root / "current.json"
        self.previous_file = root / "previous.json"

    def release_path(self, revision: str) -> Path:
        return self.releases / revision

    def publish(self, staging: Path, revision: str) -> Path:
        self.releases.mkdir(parents=True, exist_ok=True)
        destination = self.release_path(revision)
        if destination.exists():
            # Releases are immutable. Rebuilding an already-published commit must
            # never remove files from beneath readers of that release.
            shutil.rmtree(staging)
        else:
            os.replace(staging, destination)
        previous = self.current_revision()
        if previous and previous != revision:
            self._atomic_json(self.previous_file, {"source_revision": previous})
        self._atomic_json(self.current_file, {"source_revision": revision})
        return destination

    def stage(self) -> Path:
        self.root.mkdir(parents=True, exist_ok=True)
        return Path(tempfile.mkdtemp(prefix=".staging-", dir=self.root))

    def current_revision(self) -> str | None:
        if not self.current_file.is_file():
            return None
        return str(json.loads(self.current_file.read_text(encoding="utf-8"))["source_revision"])

    def rollback(self) -> str:
        if not self.previous_file.is_file():
            raise RuntimeError("no previous good index is available")
        previous = str(json.loads(self.previous_file.read_text(encoding="utf-8"))["source_revision"])
        if not self.release_path(previous).is_dir():
            raise RuntimeError(f"previous release is missing: {previous}")
        current = self.current_revision()
        self._atomic_json(self.current_file, {"source_revision": previous})
        if current:
            self._atomic_json(self.previous_file, {"source_revision": current})
        return previous

    @staticmethod
    def _atomic_json(path: Path, value: dict[str, object]) -> None:
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temporary, path)
