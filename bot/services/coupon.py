import httpx


API_URL = "http://server2.anonixvpn.space"
# API_URL = "http://backend:8000"

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

            data = response.json()

            if response.status_code == 200:
                msg = data.get("detail", "Промокод успешно применён!")
                vless = data.get("vless")
                if vless:
                    msg += f"\n\n🔗 VLESS:\n<code>{vless}</code>"
                return msg

            return data.get("detail") or data.get("error") or "Ошибка применения промокода."

        except httpx.RequestError:
            return "Сервер недоступен. Попробуйте позже."
