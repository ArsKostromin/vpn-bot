import json
import hmac
import hashlib
import httpx

# ❗ На проде всё это вынеси в .env
CRYPTOMUS_API_KEY = "WwNQW5SvFmkwozP6JTetW1VCpo5ywjoZ0DbfEgM9GfkVaXj5VS1Ey4TwPzsaUEgvQcNi7ldIhtcNF6ZchEYtIKqUFRjw8R3qkJMN9G9VB3V6vtdd0XW0dxKotU9fvtcE"
CRYPTOMUS_MERCHANT_ID = "59fc86a1-d195-4df8-8d17-3d6b06d2fe48"
CRYPTOMUS_CALLBACK_URL = "https://server2.anonixvpn.space/payments/api/crypto/webhook/"
CRYPTOMUS_RETURN_URL = "https://t.me/anonixvpn_bot"
CRYPTOMUS_NETWORK = "TRC20"  # или "BEP20", "ERC20" — смотри что у тебя в админке

async def generate_signature(data: dict) -> str:
    """Генерация подписи Cryptomus: строго без пробелов, utf-8, JSON без ASCII"""
    payload_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    return hmac.new(
        CRYPTOMUS_API_KEY.encode("utf-8"),
        payload_str.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

async def create_cryptomus_invoice(amount: int, currency: str, user_id: int) -> str:
    url = "https://api.cryptomus.com/v1/payment"

    payload = {
        "amount": str(amount),
        "currency": currency.upper(),  # ВАЖНО: USDT, BTC и т.д.
        "order_id": f"user_{user_id}_{currency}_{amount}",
        "url_callback": CRYPTOMUS_CALLBACK_URL,
        "url_return": CRYPTOMUS_RETURN_URL,
        "is_payment_multiple": False,
        "lifetime": 900,  # 15 минут (максимум 86400)
        "network": CRYPTOMUS_NETWORK,
    }

    sign = await generate_signature(payload)

    headers = {
        "merchant": CRYPTOMUS_MERCHANT_ID,
        "sign": sign,
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()  # выбросит ошибку если не 2xx
        result = response.json()
        return result["result"]["url"]
