from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Config:
    token: str

def load_config():
    return Config(token=os.getenv("BOT_TOKEN"))