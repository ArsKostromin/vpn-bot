import aiosqlite

DB_PATH = "vpn.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER UNIQUE,
                username TEXT,
                vless_link TEXT
            )
        """)
        await db.commit()

async def get_user(tg_id):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
        return await cursor.fetchone()

async def create_user(tg_id, username, vless_link):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO users (tg_id, username, vless_link) VALUES (?, ?, ?)",
            (tg_id, username, vless_link)
        )
        await db.commit()
        
        
async def init_db(db_url: str):
    # тут ты можешь логиниться в PostgreSQL, SQLite и т.д.
    pass
