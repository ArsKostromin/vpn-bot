import uuid
import time
import aiohttp
from bot.config import settings

CRYPTO_CALLBACK_URL = f"{settings.BASE_BACKEND_URL}/api/cryptomus/callback/"

async def create_payment(amount: int, user_id: int):
    """
    Создание платежа через Cryptomus API.
    Возвращает URL для оплаты.
    """
    async with aiohttp.ClientSession() as session:
        url = 'https://api.cryptomus.com/v1/payment'

        payload = {
            'amount': str(amount),
            'currency': 'USD',
            'order_id': str(uuid.uuid4()),  # уникальный ID для каждого платежа
            'url_return': 'https://t.me/YOUR_BOT_USERNAME',  # можно настроить редирект
            'url_callback': CRYPTO_CALLBACK_URL,
            'is_payment_multiple': False,
            'lifetime': 900,  # 15 минут
            'to_currency': 'USDT',
            'network': 'trc20',
            'payer_email': f"user{user_id}@bot.local",
        }

        headers = {
            'Content-Type': 'application/json',
            'merchant': settings.CRYPTOMUS_MERCHANT_UUID,
            'sign': generate_signature(payload, settings.CRYPTOMUS_API_KEY),
        }

        async with session.post(url, json=payload, headers=headers) as response:
            data = await response.json()
            if data.get("status") != "success":
                raise Exception(f"Cryptomus error: {data}")
            return data['result']['url']


def generate_signature(data: dict, api_key: str) -> str:
    """
    Генерация подписи Cryptomus.
    """
    import hmac
    import hashlib
    import json

    message = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    return hmac.new(api_key.encode(), message.encode(), hashlib.sha256).hexdigest()
