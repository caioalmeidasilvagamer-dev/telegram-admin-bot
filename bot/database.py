import aiosqlite
from loguru import logger

DB_PATH = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                username    TEXT,
                warn_count  INTEGER DEFAULT 0,
                is_banned   INTEGER DEFAULT 0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                action      TEXT,
                admin_id    INTEGER,
                target_id   INTEGER,
                reason      TEXT,
                timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
        logger.info("Banco de dados inicializado.")

async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchone()

async def upsert_user(user_id: int, username: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (user_id, username)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET username = excluded.username
        """, (user_id, username))
        await db.commit()

async def add_warn(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "UPDATE users SET warn_count = warn_count + 1 WHERE user_id = ? RETURNING warn_count",
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            await db.commit()
            return row[0] if row else 0

async def log_action(action: str, admin_id: int, target_id: int, reason: str = ""):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO logs (action, admin_id, target_id, reason) VALUES (?, ?, ?, ?)",
            (action, admin_id, target_id, reason)
        )
        await db.commit()