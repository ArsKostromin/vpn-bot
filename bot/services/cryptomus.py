import aiohttp
import logging
import json
import hmac
import hashlib
from collections import OrderedDict

CRYPTOMUS_API_KEY = "WwNQW5SvFmkwozP6JTetW1VCpo5ywjoZ0DbfEgM9GfkVaXj5VS1Ey4TwPzsaUEgvQcNi7ldIhtcNF6ZchEYtIKqUFRjw8R3qkJMN9G9VB3V6vtdd0XW0dxKotU9fvtcE"
CRYPTOMUS_MERCHANT_ID = "59fc86a1-d195-4df8-8d17-3d6b06d2fe48"
CRYPTOMUS_URL = "https://api.cryptomus.com/v1/payment"

async def create_cryptomus_invoice(user_id: int, amount: int, currency: str) -> str:
    payload_dict = {
        "amount": str(amount),
        "currency": currency.upper(),
        "order_id": str(user_id),
        "url_callback": "https://yourdomain.com/cryptomus-webhook",
        "lifetime": 3600,
        "description": f"Пополнение баланса пользователем {user_id}",
        "is_payment_multiple": False,
    }

    # Порядок ключей важен: OrderedDict
    ordered_payload = OrderedDict([
        ("amount", str(amount)),
        ("currency", currency.upper()),
        ("order_id", str(user_id)),
        ("url_callback", "https://yourdomain.com/cryptomus-webhook"),
        ("lifetime", 3600),
        ("description", f"Пополнение баланса пользователем {user_id}"),
        ("is_payment_multiple", False),
    ])

    # Строгое сериализованное тело (без пробелов)
    payload_str = json.dumps(ordered_payload, separators=(',', ':'), ensure_ascii=False)

    signature = hmac.new(
        CRYPTOMUS_API_KEY.encode(),
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()

    # DEBUG
    logging.warning(f"[Cryptomus DEBUG] Payload string (for sign): {payload_str}")
    logging.warning(f"[Cryptomus DEBUG] Signature: {signature}")

    headers = {
        "merchant": CRYPTOMUS_MERCHANT_ID,
        "sign": signature,
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(CRYPTOMUS_URL, data=payload_str, headers=headers) as resp:
            result = await resp.json()
            if result.get("status") == "success":
                return result["result"]["url"]
            else:
                logging.error(f"Cryptomus error: {result}")
                raise Exception("Не удалось создать инвойс через Cryptomus")
