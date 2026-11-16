# 🤖 discobot

[![CI](https://github.com/talhaarshadqa/discobot/actions/workflows/ci.yml/badge.svg)](https://github.com/talhaarshadqa/discobot/actions)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![discord.py](https://img.shields.io/badge/discord.py-5865F2?logo=discord&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

**A clean, extensible Discord bot in Python** — welcome messages, polls, word-filter moderation,
and bulk message purge. The command logic is kept separate from `discord.py`, so it's
**fully unit-tested** and easy to extend.

## ✨ Features

- **Welcome messages** for new members
- **Polls**: `!poll Question | Option A | Option B` with number reactions
- **Moderation**: automatic word filter with proper word-boundary matching
- **Purge**: `!purge 20` bulk-deletes messages (validated 1–100)
- **Command router** so adding a new `!command` is a few lines
- Logic layer has **no Discord dependency** → tested on Python 3.10–3.13 in CI

## 🚀 Run it

```bash
git clone https://github.com/talhaarshadqa/discobot.git
cd discobot
pip install -e .
export DISCORD_TOKEN="your-bot-token"
export BANNED_WORDS="spam,scam"      # optional
discobot
```

Create the bot and token at the [Discord Developer Portal](https://discord.com/developers/applications),
enable the **Message Content** and **Server Members** intents, and invite it to your server.

## 🧩 Commands

| Command | Description |
|---|---|
| `!ping` | Health check |
| `!poll Q \| A \| B \| ...` | Create a reaction poll (2–10 options) |
| `!purge N` | Delete the last N messages (admin) |

## 🧪 Development

The interesting logic — poll building, the command router, the word filter — lives in
`commands.py` and `moderation.py` with zero Discord imports, so the tests run instantly:

```bash
pip install -e ".[dev]"
pytest --cov=discobot
```

## 📄 License

MIT
