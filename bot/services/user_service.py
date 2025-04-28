import logging
import httpx
from typing import Optional, Tuple

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Можно поставить DEBUG на разработке


API_URL = "https://vpnbot.onrender.com"
# API_URL = "http://backend:8000"


async def register_user_via_api(telegram_id: int) -> Optional[Tuple[str, bool]]:
    url = f"{API_URL}/user/api/register/"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json={"telegram_id": telegram_id})
            response.raise_for_status()
            data = response.json()
            return data.get("link_code"), data.get("created")
        except httpx.HTTPStatusError as e:
            logger.error(f"Ошибка регистрации пользователя {telegram_id}: {e.response.status_code} — {e.response.text}")
        except Exception as e:
            logger.error(f"Неизвестная ошибка при регистрации пользователя {telegram_id}: {e}")
    return None

async def get_user_subscriptions(telegram_id: int) -> list[dict]:
    url = f"{API_URL}/user/user-subscriptions/{telegram_id}/"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Ошибка получения подписок для пользователя {telegram_id}: {e.response.status_code} — {e.response.text}")
        except Exception as e:
            logger.error(f"Неизвестная ошибка при получении подписок пользователя {telegram_id}: {e}")
    return []


async def get_user_info(telegram_id: int) -> dict:
    url = f"{API_URL}/user/user-info/{telegram_id}/"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Ошибка получения информации о пользователе {telegram_id}: {e.response.status_code} — {e.response.text}")
        except Exception as e:
            logger.error(f"Неизвестная ошибка при получении информации о пользователе {telegram_id}: {e}")
    return {}