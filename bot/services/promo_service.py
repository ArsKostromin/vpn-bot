import httpx
import logging

logger = logging.getLogger(__name__)

API_URL = "https://admin.byebyefbi.com"

async def get_promo_code_from_api(user_id: int) -> dict:
    url = f"{API_URL}/coupon/generate_promo/"
    payload = {"telegram_id": user_id}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return {"promo_code": data.get("promo_code"), "error": data.get("error")}
        except httpx.HTTPStatusError as e:
            try:
                data = e.response.json()
                return {"promo_code": None, "error": data.get("error")}
            except Exception:
                pass
            logger.error(f"Ошибка при получении промокода для {user_id}: {e}")
            return {"promo_code": None, "error": str(e)}
        except Exception as e:
            logger.error(f"Ошибка при получении промокода для {user_id}: {e}")
            return {"promo_code": None, "error": str(e)}
