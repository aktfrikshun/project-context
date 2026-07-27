from __future__ import annotations

import hashlib
import math
import re
from abc import ABC, abstractmethod

TOKEN = re.compile(r"[\w'-]+", re.UNICODE)


def tokens(text: str) -> list[str]:
    return [token.casefold() for token in TOKEN.findall(text)]


class EmbeddingAdapter(ABC):
    name = "abstract"

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        raise NotImplementedError


class HashEmbeddingAdapter(EmbeddingAdapter):
    """Credential-free semantic-ish projection used as a deterministic fallback."""

    name = "hash-v1"

    def __init__(self, dimensions: int = 256):
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        terms = tokens(text)
        for term in terms:
            digest = hashlib.sha256(term.encode()).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = -1.0 if digest[4] & 1 else 1.0
            vector[index] += sign
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [round(value / norm, 8) for value in vector]


def cosine(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        return 0.0
    return sum(a * b for a, b in zip(left, right))
