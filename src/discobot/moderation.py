"""A simple word filter for moderation."""
from __future__ import annotations
import re


class WordFilter:
    def __init__(self, banned: list[str]) -> None:
        self._banned = [b.lower() for b in banned if b.strip()]
        joined = "|".join(re.escape(b) for b in self._banned)
        self._re = re.compile(rf"(?<!\w)({joined})(?!\w)", re.IGNORECASE) if joined else None

    def matches(self, text: str) -> list[str]:
        if not self._re:
            return []
        return [m.group(0).lower() for m in self._re.finditer(text)]

    def is_clean(self, text: str) -> bool:
        return not self.matches(text)
