import aiohttp
import logging

CRYPTOMUS_API_KEY = "WwNQW5SvFmkwozP6JTetW1VCpo5ywjoZ0DbfEgM9GfkVaXj5VS1Ey4TwPzsaUEgvQcNi7ldIhtcNF6ZchEYtIKqUFRjw8R3qkJMN9G9VB3V6vtdd0XW0dxKotU9fvtcE"
CRYPTOMUS_MERCHANT_ID = "59fc86a1-d195-4df8-8d17-3d6b06d2fe48"
CRYPTOMUS_URL = "https://api.cryptomus.com/v1/payment"

async def create_cryptomus_invoice(user_id: int, amount: int, currency: str) -> str:
    payload = {
        "amount": str(amount),
        "currency": currency.upper(),  # "USDT", "TON", "BTC", и т.д.
        "order_id": str(user_id),
        "url_callback": "https://yourdomain.com/cryptomus-webhook",
        "lifetime": 3600,
        "description": f"Пополнение баланса пользователем {user_id}",
        "is_payment_multiple": False,
    }

    headers = {
        "merchant": CRYPTOMUS_MERCHANT_ID,
        "sign": "GENERATED_SIGNATURE",  # подпись если хочешь заморочиться, Cryptomus требует sign
        "Content-Type": "application/json",
        "accept": "application/json",
        "api-key": CRYPTOMUS_API_KEY
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(CRYPTOMUS_URL, json=payload, headers=headers) as resp:
            result = await resp.json()
            if result.get("status") == "success":
                return result["result"]["url"]
            else:
                logging.error(f"Cryptomus error: {result}")
                raise Exception("Не удалось создать инвойс через Cryptomus")
