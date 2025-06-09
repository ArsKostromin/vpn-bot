import httpx
import logging

logger = logging.getLogger(__name__)

API_URL = "http://server2.anonixvpn.space"

async def get_promo_code_from_api(user_id: int) -> str:
    url = f"{API_URL}/coupon/generate_promo/"
    payload = {"telegram_id": user_id}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json().get("promo_code", "VPNFREE")
        except Exception as e:
            logger.error(f"Ошибка при получении промокода для {user_id}: {e}")
            return "VPNFREE"
