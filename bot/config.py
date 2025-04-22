from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class BotConfig:
    token: str
    use_redis: bool = False  # на будущее

@dataclass
class DBConfig:
    url: str  # например, "sqlite+aiosqlite:///db.sqlite3" или PostgreSQL URL

@dataclass
class Config:
    bot: BotConfig
    db: DBConfig

def load_config() -> Config:
    return Config(
        bot=BotConfig(token=os.getenv("BOT_TOKEN")),
        db=DBConfig(url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3"))
    )
