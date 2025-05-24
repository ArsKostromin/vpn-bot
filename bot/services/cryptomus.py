import asyncio
import base64
import hashlib
import json
import logging
import aiohttp
from aiogram.types import Message

CRYPTOMUS_API_KEY = "WwNQW5SvFmkwozP6JTetW1VCpo5ywjoZ0DbfEgM9GfkVaXj5VS1Ey4TwPzsaUEgvQcNi7ldIhtcNF6ZchEYtIKqUFRjw8R3qkJMN9G9VB3V6vtdd0XW0dxKotU9fvtcE"
CRYPTOMUS_MERCHANT_ID = "59fc86a1-d195-4df8-8d17-3d6b06d2fe48"

logging.basicConfig(level=logging.DEBUG)


async def make_request(url: str, invoice_data: dict):
    encoded_data = base64.b64encode(
        json.dumps(invoice_data).encode("utf-8")
    ).decode("utf-8")
    signature = hashlib.md5(
        f"{encoded_data}{CRYPTOMUS_API_KEY}".encode("utf-8")
    ).hexdigest()

    headers = {
        "merchant": CRYPTOMUS_MERCHANT_ID,
        "sign": signature,
    }

    logging.debug(f"Sending request to Cryptomus: {url} | headers={headers} | data={invoice_data}")

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url=url, json=invoice_data) as response:
            text = await response.text()
            logging.debug(f"Cryptomus raw response: {text}")
            if not response.ok:
                raise ValueError(f"Ошибка запроса: {response.status} {text}")
            return json.loads(text)


async def check_invoice_paid(uuid: str, message: Message):
    while True:
        try:
            invoice_data = await make_request(
                url="https://api.cryptomus.com/v1/payment/info",
                invoice_data={"uuid": uuid},
            )

            status = invoice_data["result"].get("payment_status")
            logging.info(f"Invoice status: {status} | uuid={uuid}")

            if status in ("paid", "paid_over"):
                await message.answer("✅ Оплата прошла успешно! Спасибо!")
                return
            else:
                logging.debug(f"🕓 Платёж ещё не прошёл: {status}")
        except Exception as e:
            logging.error(f"Ошибка при проверке статуса: {e}", exc_info=True)

        await asyncio.sleep(10)