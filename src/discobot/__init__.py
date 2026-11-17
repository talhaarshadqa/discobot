"""discobot - a Python Discord bot with testable command logic."""
from .commands import Router, build_welcome, make_poll, parse_purge_amount
from .moderation import WordFilter

__all__ = ["Router", "WordFilter", "build_welcome", "make_poll", "parse_purge_amount"]
__version__ = "1.0.0"
