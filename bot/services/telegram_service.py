from aiogram import Bot
from aiogram.types import ChatMember
from bot.config import CHANNEL_USERNAME
import logging

async def is_user_subscribed(bot: Bot, user_id: int) -> bool:
    try:
        member: ChatMember = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logging.warning(f"Ошибка проверки подписки пользователя {user_id} в канале {CHANNEL_USERNAME}: {e}")
        return False
