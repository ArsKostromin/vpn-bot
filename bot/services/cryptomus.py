import asyncio
import base64
import hashlib
import json
import logging
import aiohttp
from aiogram.types import Message
import urllib.parse

CRYPTOMUS_API_KEY = "WwNQW5SvFmkwozP6JTetW1VCpo5ywjoZ0DbfEgM9GfkVaXj5VS1Ey4TwPzsaUEgvQcNi7ldIhtcNF6ZchEYtIKqUFRjw8R3qkJMN9G9VB3V6vtdd0XW0dxKotU9fvtcE"
CRYPTOMUS_MERCHANT_ID = "59fc86a1-d195-4df8-8d17-3d6b06d2fe48"

logging.basicConfig(level=logging.DEBUG)


def generate_qr_code_url(address: str, amount: str = None, currency: str = None) -> str:
    """
    Генерирует URL для QR-кода на основе адреса кошелька
    """
    try:
        # Базовый URL для генерации QR-кода
        base_url = "https://api.qrserver.com/v1/create-qr-code/"
        
        # Формируем данные для QR-кода
        qr_data = address
        if amount and currency:
            # Для некоторых криптовалют можно добавить сумму
            if currency.upper() in ["BTC", "ETH", "TON", "LTC"]:
                qr_data = f"{address}?amount={amount}"
        
        # Кодируем данные для URL
        encoded_data = urllib.parse.quote(qr_data)
        
        # Формируем полный URL
        qr_url = f"{base_url}?size=200x200&data={encoded_data}"
        
        return qr_url
    except Exception as e:
        logging.error(f"Ошибка при генерации QR-кода: {e}")
        return ""


async def make_request(url: str, invoice_data: dict):
    encoded_data = base64.b64encode(
        json.dumps(invoice_data).encode("utf-8")
    ).decode("utf-8")
    
    # Используем SHA256 для подписи (Cryptomus требует SHA256)
    signature = hashlib.sha256(
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


def extract_wallet_info(response_data: dict) -> dict:
    """
    Извлекает информацию о кошельке и QR-коде из ответа Cryptomus
    """
    try:
        result = response_data.get("result", {})
        payment_address = result.get("payment_address", "")
        payment_amount = result.get("payment_amount", "")
        payment_currency = result.get("payment_currency", "")
        qr_code = result.get("qr_code", "")
        
        # Проверяем, что у нас есть адрес
        if not payment_address:
            logging.warning("Адрес кошелька не найден в ответе Cryptomus")
            return {}
        
        # Если QR-код не предоставлен, генерируем его
        if not qr_code and payment_address:
            qr_code = generate_qr_code_url(payment_address, payment_amount, payment_currency)
            logging.info(f"Сгенерирован QR-код для адреса: {payment_address[:10]}...")
        
        return {
            "address": payment_address,
            "amount": payment_amount,
            "currency": payment_currency,
            "qr_code": qr_code,
            "uuid": result.get("uuid", "")
        }
    except Exception as e:
        logging.error(f"Ошибка при извлечении информации о кошельке: {e}")
        return {}


async def check_invoice_paid(uuid: str, message: Message, state=None):
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
                # Очищаем состояние если оно передано
                if state:
                    await state.clear()
                return
            else:
                logging.debug(f"🕓 Платёж ещё не прошёл: {status}")
        except Exception as e:
            logging.error(f"Ошибка при проверке статуса: {e}", exc_info=True)

        await asyncio.sleep(10)