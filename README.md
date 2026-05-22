# 🤖 Telegram Admin Bot

A feature-rich Telegram group/channel admin bot built with Python, designed to automate moderation and management tasks. Built with `python-telegram-bot` v20+ using fully async architecture.

---

## ✨ Features

- **Welcome messages** — Automatically greets new members when they join via invite link
- **Warn system** — Issue warnings to users; auto-ban triggers at 3 warnings
- **Ban system** — Permanently ban users with optional reason logging
- **Mute system** — Temporarily restrict users for a configurable duration
- **Anti-flood protection** — Automatically mutes users who send 5+ messages within 10 seconds
- **User info** — Retrieve a user's warning count and ban status from the database
- **Action logging** — All moderation actions are logged to a SQLite database with timestamps

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `python-telegram-bot` v20+ | Telegram Bot API wrapper (async) |
| `aiosqlite` | Async SQLite database |
| `python-dotenv` | Environment variable management |
| `loguru` | Structured logging |

---

## 📁 Project Structure

```
telegram-admin-bot/
├── bot/
│   ├── main.py            # Entry point
│   ├── config.py          # Environment config
│   ├── database.py        # SQLite operations
│   ├── handlers/
│   │   ├── admin.py       # /warn, /ban, /mute, /info
│   │   ├── moderation.py  # Anti-flood
│   │   └── welcome.py     # New member handler
│   └── utils/
│       └── helpers.py     # admin_only decorator
├── logs/
├── .env.example
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

**1. Clone the repository**
```bash
git clone https://github.com/caioalmeidasilvagamer-dev/telegram-admin-bot.git
cd telegram-admin-bot
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` with your values:
```
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_IDS=your_telegram_user_id
```

- Get your bot token from [@BotFather](https://t.me/BotFather)
- Get your Telegram user ID from [@userinfobot](https://t.me/userinfobot)

**4. Run the bot**
```bash
python -m bot.main
```

---

## 📋 Commands

| Command | Description | Usage |
|---|---|---|
| `/warn` | Warn a user (auto-bans at 3) | Reply to a message |
| `/ban` | Permanently ban a user | `/ban reason` as reply |
| `/mute` | Temporarily mute a user | `/mute 30 reason` as reply |
| `/info` | View user moderation history | Reply to a message |

> All commands require the user to be listed in `ADMIN_IDS`.

---

## 🗄️ Database Schema

```sql
-- Tracks users and their moderation status
CREATE TABLE users (
    user_id     INTEGER PRIMARY KEY,
    username    TEXT,
    warn_count  INTEGER DEFAULT 0,
    is_banned   INTEGER DEFAULT 0
);

-- Logs all moderation actions
CREATE TABLE logs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    action      TEXT,
    admin_id    INTEGER,
    target_id   INTEGER,
    reason      TEXT,
    timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## ⚠️ Known Limitations

- Admin commands require replying to a message — if the original message was deleted, the command cannot be executed. A future improvement would be to also accept `/ban <user_id>` as a fallback.
- `message_tracker` (anti-flood memory) resets when the bot restarts.
- Currently supports a single group per bot instance.

---

## 📄 License

MIT