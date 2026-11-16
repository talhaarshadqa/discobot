"""discord.py adapter. Imported lazily so the package installs without a token."""
from __future__ import annotations
import os

from .commands import Router, build_welcome, make_poll, parse_purge_amount
from .moderation import WordFilter

router = Router()


@router.command("ping")
def _ping(args: str) -> str:
    return "\U0001F3D3 Pong!"


@router.command("poll")
def _poll(args: str) -> str:
    q, *opts = [p.strip() for p in args.split("|")]
    return make_poll(q, opts).render()


def run(token: str | None = None) -> None:  # pragma: no cover - needs a live gateway
    import discord
    from discord.ext import commands

    token = token or os.environ["DISCORD_TOKEN"]
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    wordfilter = WordFilter(os.getenv("BANNED_WORDS", "").split(","))

    @bot.event
    async def on_member_join(member):
        if member.guild.system_channel:
            await member.guild.system_channel.send(build_welcome(member.mention, member.guild.name))

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        if wordfilter.matches(message.content):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, please keep it civil.", delete_after=5)
            return
        reply = router.dispatch(message.content)
        if reply:
            await message.channel.send(reply)

    @bot.command(name="purge")
    async def purge(ctx, amount: str):
        n = parse_purge_amount(amount)
        await ctx.channel.purge(limit=n + 1)
        await ctx.send(f"Deleted {n} messages.", delete_after=5)

    bot.run(token)
