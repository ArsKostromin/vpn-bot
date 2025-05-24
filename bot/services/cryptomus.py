import asyncio
import base64
import hashlib
import json
import uuid

import aiohttp

CRYPTOMUS_API_KEY = "WwNQW5SvFmkwozP6JTetW1VCpo5ywjoZ0DbfEgM9GfkVaXj5VS1Ey4TwPzsaUEgvQcNi7ldIhtcNF6ZchEYtIKqUFRjw8R3qkJMN9G9VB3V6vtdd0XW0dxKotU9fvtcE"
CRYPTOMUS_MERCHANT_UUID = "59fc86a1-d195-4df8-8d17-3d6b06d2fe48"
CRYPTO_CALLBACK_URL = "https://server2.anonixvpn.space/payments/api/crypto/webhook/"
CRYPTO_RETURN_URL = "https://t.me/fastvpnVPNs_bot"


async def make_request(url: str, invoice_data: dict):
    encoded_data = base64.b64encode(
        json.dumps(invoice_data).encode("utf-8")
    ).decode("utf-8")

    sign = hashlib.md5(f"{encoded_data}{CRYPTOMUS_API_KEY}".encode("utf-8")).hexdigest()

    headers = {
        "merchant": CRYPTOMUS_MERCHANT_UUID,
        "sign": sign,
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, json=invoice_data) as response:
            data = await response.json()
            if not response.ok or data.get("status") != "success":
                raise Exception(f"Cryptomus error: {data}")
            return data


async def create_payment(amount: int, user_id: int):
    payload = {
        "amount": str(amount),
        "currency": "USDT",
        "order_id": f"user_{user_id}_{amount}",
        "url_callback": CRYPTO_CALLBACK_URL,
        "url_return": CRYPTO_RETURN_URL,
        "is_payment_multiple": False,
        "lifetime": 900,
        "network": "TRC20",
    }

    url = "https://api.cryptomus.com/v1/payment"
    result = await make_request(url, payload)
    return result["result"]["url"]


async def check_invoice_paid(invoice_id: str) -> bool:
    url = "https://api.cryptomus.com/v1/payment/info"
    payload = {"uuid": invoice_id}
    result = await make_request(url, payload)
    return result.get("result", {}).get("payment_status") in ("paid", "paid_over")
