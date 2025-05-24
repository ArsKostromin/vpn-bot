import uuid
import aiohttp
import hmac
import hashlib
import json

CRYPTOMUS_API_KEY = "WwNQW5SvFmkwozP6JTetW1VCpo5ywjoZ0DbfEgM9GfkVaXj5VS1Ey4TwPzsaUEgvQcNi7ldIhtcNF6ZchEYtIKqUFRjw8R3qkJMN9G9VB3V6vtdd0XW0dxKotU9fvtcE"
CRYPTOMUS_MERCHANT_UUID = "59fc86a1-d195-4df8-8d17-3d6b06d2fe48"
CRYPTO_CALLBACK_URL = "https://server2.anonixvpn.space/payments/api/crypto/webhook/"


def generate_signature(data: dict, api_key: str) -> str:
    # json.dumps возвращает строку, которая должна быть в точности такой же, как тело запроса
    message = json.dumps(data, separators=(',', ':'), ensure_ascii=False, sort_keys=True)
    return hmac.new(api_key.encode(), message.encode(), hashlib.sha256).hexdigest()



async def make_request(endpoint: str, payload: dict):
    url = f"https://api.cryptomus.com/v1/{endpoint}"

    # ВАЖНО: фиксируем порядок ключей при генерации подписи
    signature_payload = json.loads(json.dumps(payload, separators=(',', ':'), ensure_ascii=False, sort_keys=True))
    sign = generate_signature(signature_payload, CRYPTOMUS_API_KEY)

    headers = {
        "Content-Type": "application/json",
        "merchant": CRYPTOMUS_MERCHANT_UUID,
        "sign": sign,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=signature_payload, headers=headers) as response:
            data = await response.json()
            if data.get("status") != "success":
                raise Exception(f"Cryptomus error: {data}")
            return data



async def create_payment(amount: int, user_id: int):
    payload = {
        'amount': str(amount),
        'currency': 'USD',
        'order_id': str(uuid.uuid4()),
        'url_return': 'https://t.me/YOUR_BOT_USERNAME',
        'url_callback': CRYPTO_CALLBACK_URL,
        'is_payment_multiple': False,
        'lifetime': 900,
        'to_currency': 'USDT',
        'network': 'trc20',
        'payer_email': f"user{user_id}@bot.local",
    }

    result = await make_request("payment", payload)
    return result["url"]


async def check_invoice_paid(invoice_id: str) -> bool:
    payload = {"uuid": invoice_id}
    result = await make_request("payment/info", payload)
    return result.get("status") == "paid"
