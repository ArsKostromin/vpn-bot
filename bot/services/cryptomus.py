import aiohttp
import logging
import json
import hmac
import hashlib
import httpx

CRYPTOMUS_API_KEY = "WwNQW5SvFmkwozP6JTetW1VCpo5ywjoZ0DbfEgM9GfkVaXj5VS1Ey4TwPzsaUEgvQcNi7ldIhtcNF6ZchEYtIKqUFRjw8R3qkJMN9G9VB3V6vtdd0XW0dxKotU9fvtcE"
CRYPTOMUS_MERCHANT_ID = "59fc86a1-d195-4df8-8d17-3d6b06d2fe48"
CRYPTOMUS_CALLBACK_URL = "https://server2.anonixvpn.space/payments/api/crypto/webhook/"
 

async def create_cryptomus_invoice(amount: int, currency: str, user_id: int) -> str:
    url = "https://api.cryptomus.com/v1/payment"

    payload = {
        "amount": str(amount),
        "currency": currency,
        "order_id": f"user_{user_id}_{currency}_{amount}",
        "url_callback": CRYPTOMUS_CALLBACK_URL,
    }

    headers = {
        "merchant": CRYPTOMUS_MERCHANT_ID,
        "sign": await generate_signature(payload),
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["result"]["url"]


import hmac
import hashlib
import json

async def generate_signature(data: dict) -> str:
    payload_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    return hmac.new(
        CRYPTOMUS_API_KEY.encode(),
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()