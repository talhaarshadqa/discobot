import pytest

from discobot.commands import Router, build_welcome, make_poll, parse_purge_amount
from discobot.moderation import WordFilter


def test_welcome():
    out = build_welcome("@sam", "Devs")
    assert "@sam" in out and "Devs" in out


def test_make_poll():
    p = make_poll("Best language?", ["Python", "Go", "Rust"])
    assert p.reactions[:3] == ["1⃣", "2⃣", "3⃣"]
    rendered = p.render()
    assert "Best language?" in rendered and "Python" in rendered
    with pytest.raises(ValueError):
        make_poll("only one", ["a"])
    with pytest.raises(ValueError):
        make_poll("", ["a", "b"])


@pytest.mark.parametrize("arg,expected", [("5", 5), ("100", 100), ("1", 1)])
def test_purge_ok(arg, expected):
    assert parse_purge_amount(arg) == expected


@pytest.mark.parametrize("arg", ["0", "101", "-3", "abc", ""])
def test_purge_bad(arg):
    with pytest.raises(ValueError):
        parse_purge_amount(arg)


def test_router():
    r = Router(prefix="!")

    @r.command("hello")
    def hello(args):
        return f"hi {args}" if args else "hi"

    assert r.dispatch("!hello world") == "hi world"
    assert r.dispatch("!hello") == "hi"
    assert r.dispatch("hello") is None          # no prefix
    assert r.dispatch("!unknown x") is None     # unregistered


def test_word_filter():
    wf = WordFilter(["spam", "scam"])
    assert wf.matches("this is SPAM") == ["spam"]
    assert wf.is_clean("a normal message")
    assert wf.is_clean("scamper")               # word boundary: not a match
    assert WordFilter([]).is_clean("anything")


def test_bot_router_registers():
    from discobot.bot import router
    assert router.dispatch("!ping") == "\U0001F3D3 Pong!"
    poll_out = router.dispatch("!poll Tabs or spaces? | Tabs | Spaces")
    assert "Tabs" in poll_out and "Spaces" in poll_out
