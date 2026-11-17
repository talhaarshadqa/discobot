"""Command logic, kept free of any Discord import so it can be unit-tested."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

NUMBER_EMOJI = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣",
                "6⃣", "7⃣", "8⃣", "9⃣", "\U0001F51F"]


def build_welcome(member_name: str, guild_name: str) -> str:
    return (f"\U0001F44B Welcome to **{guild_name}**, {member_name}! "
            f"Please read the rules and introduce yourself.")


@dataclass
class Poll:
    question: str
    options: list[str]
    reactions: list[str]

    def render(self) -> str:
        lines = [f"\U0001F4CA **{self.question}**", ""]
        for emoji, opt in zip(self.reactions, self.options):
            lines.append(f"{emoji}  {opt}")
        return "\n".join(lines)


def make_poll(question: str, options: list[str]) -> Poll:
    options = [o.strip() for o in options if o.strip()]
    if not question.strip():
        raise ValueError("poll needs a question")
    if not 2 <= len(options) <= 10:
        raise ValueError("a poll needs between 2 and 10 options")
    return Poll(question.strip(), options, NUMBER_EMOJI[: len(options)])


def parse_purge_amount(arg: str) -> int:
    try:
        n = int(arg)
    except (TypeError, ValueError):
        raise ValueError("amount must be a whole number") from None
    if not 1 <= n <= 100:
        raise ValueError("amount must be between 1 and 100")
    return n


class Router:
    """Maps '!command args' strings to handlers. Handlers take (args:str)."""

    def __init__(self, prefix: str = "!") -> None:
        self.prefix = prefix
        self._handlers: dict[str, Callable[[str], str]] = {}

    def command(self, name: str) -> Callable:
        def deco(fn: Callable[[str], str]) -> Callable[[str], str]:
            self._handlers[name] = fn
            return fn
        return deco

    def dispatch(self, message: str) -> str | None:
        if not message.startswith(self.prefix):
            return None
        body = message[len(self.prefix):]
        name, _, args = body.partition(" ")
        handler = self._handlers.get(name.lower())
        if handler is None:
            return None
        return handler(args.strip())
