import json
import hmac
import hashlib
import httpx
import logging

# Настраиваем логгер
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # если хочешь DEBUG — меняй уровень

# ❗ На проде — в .env, а не так!
CRYPTOMUS_API_KEY = "WwNQW5SvFmkwozP6JTetW1VCpo5ywjoZ0DbfEgM9GfkVaXj5VS1Ey4TwPzsaUEgvQcNi7ldIhtcNF6ZchEYtIKqUFRjw8R3qkJMN9G9VB3V6vtdd0XW0dxKotU9fvtcE"
CRYPTOMUS_MERCHANT_ID = "59fc86a1-d195-4df8-8d17-3d6b06d2fe48"
CRYPTOMUS_CALLBACK_URL = "https://server2.anonixvpn.space/payments/api/crypto/webhook/"
CRYPTOMUS_RETURN_URL = "https://t.me/fastvpnVPNs_bot"
CRYPTOMUS_NETWORK = "TRC20"

async def generate_signature(data: dict) -> str:
    """Генерация подписи Cryptomus"""
    payload_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    signature = hmac.new(
        CRYPTOMUS_API_KEY.encode("utf-8"),
        payload_str.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    logger.debug(f"[SIGNATURE] Payload: {payload_str}")
    logger.debug(f"[SIGNATURE] Generated: {signature}")
    return signature

async def create_cryptomus_invoice(amount: int, currency: str, user_id: int) -> str:
    """Создание счёта и возврат ссылки"""
    url = "https://api.cryptomus.com/v1/payment"

    payload = {
        "amount": str(amount),
        "currency": currency.upper(),
        "order_id": f"user_{user_id}_{currency}_{amount}",
        "url_callback": CRYPTOMUS_CALLBACK_URL,
        "url_return": CRYPTOMUS_RETURN_URL,
        "is_payment_multiple": False,
        "lifetime": 900,
        "network": CRYPTOMUS_NETWORK,
    }

    logger.info(f"[CREATE INVOICE] Payload: {payload}")

    sign = await generate_signature(payload)

    headers = {
        "merchant": CRYPTOMUS_MERCHANT_ID,
        "sign": sign,
        "Content-Type": "application/json",
    }

    logger.debug(f"[REQUEST] Headers: {headers}")

    async with httpx.AsyncClient() as client:
        logger.info("[HTTPX] Sending request to Cryptomus...")
        response = await client.post(url, json=payload, headers=headers)
        logger.info(f"[HTTPX] Status: {response.status_code}")
        logger.debug(f"[HTTPX] Response Text: {response.text}")

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"[HTTPX] Request failed: {e}")
            raise

        result = response.json()
        if result.get("status") != "success":
            logger.error(f"[CRYPTOMUS] Error response: {result}")
            raise Exception(f"Cryptomus error: {result}")

        invoice_url = result["result"]["url"]
        logger.info(f"[CRYPTOMUS] Payment URL: {invoice_url}")
        return invoice_url
