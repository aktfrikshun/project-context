from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Document:
    path: str
    title: str
    text: str
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class Section:
    heading: str
    heading_path: tuple[str, ...]
    level: int
    body: str

