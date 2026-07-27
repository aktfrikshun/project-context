from __future__ import annotations

import re
from pathlib import Path

from .build import BASELINE_FILES, build_chunks, discover
from .markdown import load_document

LINK = re.compile(r"(?<!!)\[[^\]]*]\(([^)#]+)(?:#[^)]+)?\)")
ALLOWED_STATUS = {
    "active", "accepted", "complete", "draft", "proposed", "deprecated",
    "superseded", "rejected",
}


def validate(root: Path, source_revision: str = "validation") -> list[str]:
    errors: list[str] = []
    for relative in BASELINE_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required baseline source: {relative}")
    paths = discover(root)
    if not paths:
        errors.append("no Chloe Markdown documents found")
        return errors
    ids: set[str] = set()
    for chunk in build_chunks(root, source_revision):
        chunk_id = str(chunk["id"])
        if chunk_id in ids:
            errors.append(f"duplicate chunk id: {chunk_id}")
        ids.add(chunk_id)
    for path in paths:
        document = load_document(root, path)
        status = str(document.metadata.get("status", "")).lower()
        if status and status not in ALLOWED_STATUS:
            errors.append(f"{document.path}: unknown front-matter status {status!r}")
        for target in LINK.findall(document.text):
            if "://" in target or target.startswith(("mailto:", "/")):
                continue
            linked = (path.parent / target).resolve()
            try:
                linked.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{document.path}: link escapes repository: {target}")
                continue
            if not linked.exists():
                errors.append(f"{document.path}: broken link: {target}")
    return errors

