"""discobot - a Python Discord bot with testable command logic."""
from .commands import build_welcome, make_poll, parse_purge_amount, Router
from .moderation import WordFilter

__all__ = ["build_welcome", "make_poll", "parse_purge_amount", "Router", "WordFilter"]
__version__ = "1.0.0"
