import aiohttp
import logging
import json
import hmac
import hashlib

CRYPTOMUS_API_KEY = "WwNQW5SvFmkwozP6JTetW1VCpo5ywjoZ0DbfEgM9GfkVaXj5VS1Ey4TwPzsaUEgvQcNi7ldIhtcNF6ZchEYtIKqUFRjw8R3qkJMN9G9VB3V6vtdd0XW0dxKotU9fvtcE"
CRYPTOMUS_MERCHANT_ID = "59fc86a1-d195-4df8-8d17-3d6b06d2fe48"
CRYPTOMUS_URL = "https://api.cryptomus.com/v1/invoice"

def json_dumps_cryptomus(data: dict) -> str:
    """
    Сериализация под Cryptomus:
    - false вместо False
    - null вместо None
    - ключи отсортированы
    - минимальные разделители
    """
    json_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False, sort_keys=True)
    json_str = json_str.replace("False", "false").replace("True", "true").replace("None", "null")
    return json_str

async def create_cryptomus_invoice(user_id: int, amount: int, currency: str) -> str:
    payload_dict = {
        "amount": str(amount),
        "currency": currency.upper(),
        "order_id": str(user_id),
        "url_callback": "https://server2.anonixvpn.space/payments/api/crypto/webhook/",
        "lifetime": 3600,
        "description": f"Пополнение баланса пользователем {user_id}",
        "is_payment_multiple": False,
    }

    payload_str = json_dumps_cryptomus(payload_dict)

    signature = hmac.new(
        CRYPTOMUS_API_KEY.encode(),
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()

    logging.warning(f"[Cryptomus DEBUG] Payload string (for sign): {payload_str}")
    logging.warning(f"[Cryptomus DEBUG] Signature: {signature}")

    headers = {
        "merchant": CRYPTOMUS_MERCHANT_ID,
        "sign": signature,
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(CRYPTOMUS_URL, json=payload_dict, headers=headers) as resp:
            try:
                result = await resp.json()
            except Exception as e:
                text = await resp.text()
                logging.error(f"Cryptomus response decode error: {e}, body: {text}")
                raise

            logging.warning(f"[Cryptomus DEBUG] Response: {result}")
            if result.get("status") == "success":
                return result["result"]["url"]
            else:
                logging.error(f"Cryptomus error: {result}")
                raise Exception("Не удалось создать инвойс через Cryptomus")
