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


CRYPTOMUS_API_KEY = "WwNQW5SvFmkwozP6JTetW1VCpo5ywjoZ0DbfEgM9GfkVaXj5VS1Ey4TwPzsaUEgvQcNi7ldIhtcNF6ZchEYtIKqUFRjw8R3qkJMN9G9VB3V6vtdd0XW0dxKotU9fvtcE"
CRYPTOMUS_MERCHANT_UUID = "59fc86a1-d195-4df8-8d17-3d6b06d2fe48"
BASE_BACKEND_URL = "https://server2.anonixvpn.space/payments/api/crypto/webhook/"


CHANNEL_USERNAME = "@anonix_vpn"