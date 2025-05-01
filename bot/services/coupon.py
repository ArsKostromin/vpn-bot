import httpx


# API_URL = "http://159.198.77.150:8000/vpn
API_URL = "http://backend:8000"

async def apply_coupon(code: str, telegram_id: int) -> str:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f'{API_URL}/coupon/apply-coupon/',
                json={
                    "code": code,
                    "telegram_id": telegram_id
                },
                timeout=10.0
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("detail", "Промокод успешно применён!")

            # Ошибки
            data = response.json()
            return data.get("detail") or data.get("error") or "Ошибка применения промокода."

        except httpx.RequestError:
            return "Сервер недоступен. Попробуйте позже."
