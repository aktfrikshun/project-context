from __future__ import annotations

import re
from pathlib import Path

from .model import Document, Section

HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
LIST_VALUE = re.compile(r"^\[(.*)]$")


def _scalar(value: str) -> object:
    value = value.strip()
    if not value:
        return ""
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    list_match = LIST_VALUE.match(value)
    if list_match:
        return [item.strip().strip("'\"") for item in list_match.group(1).split(",") if item.strip()]
    return value.strip("'\"")


def split_front_matter(text: str) -> tuple[dict[str, object], str]:
    lines = text.splitlines()
    start = 1 if lines and lines[0].lstrip().startswith("<!--") else 0
    if start and "-->" not in lines[0]:
        while start < len(lines) and "-->" not in lines[start]:
            start += 1
        start += 1
    if start >= len(lines) or lines[start].strip() != "---":
        return {}, text
    end = start + 1
    while end < len(lines) and lines[end].strip() != "---":
        end += 1
    if end == len(lines):
        return {}, text
    metadata: dict[str, object] = {}
    for line in lines[start + 1 : end]:
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = _scalar(value)
    body = "\n".join(lines[end + 1 :]).strip() + "\n"
    return metadata, body


def load_document(root: Path, path: Path) -> Document:
    raw = path.read_text(encoding="utf-8")
    metadata, body = split_front_matter(raw)
    title = str(metadata.get("title", ""))
    if not title:
        for line in body.splitlines():
            match = HEADING.match(line)
            if match:
                title = match.group(2)
                break
    return Document(path=path.relative_to(root).as_posix(), title=title or path.stem, text=body, metadata=metadata)


def sections(document: Document) -> list[Section]:
    output: list[Section] = []
    stack: list[str] = []
    current_heading = document.title
    current_level = 1
    current_path = (document.title,)
    body: list[str] = []
    in_fence = False

    def flush() -> None:
        content = "\n".join(body).strip()
        if content:
            output.append(Section(current_heading, current_path, current_level, content))

    for line in document.text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
        match = None if in_fence else HEADING.match(line)
        if not match:
            body.append(line)
            continue
        flush()
        body = []
        current_level = len(match.group(1))
        current_heading = match.group(2).strip()
        stack = stack[: current_level - 1]
        stack.append(current_heading)
        current_path = tuple(stack)
    flush()
    return output

