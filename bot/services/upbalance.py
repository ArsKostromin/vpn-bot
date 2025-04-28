import aiohttp

API_URL = "https://vpnbot.onrender.com"  # У тебя в докере так
# API_URL = "http://backend:8000"

async def create_payment_link(telegram_id: int, amount: int) -> str:
    url = f"{API_URL}/payments/create-payment/"
    data = {
        "telegram_id": telegram_id,
        "amount": amount
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result.get("payment_url")
            else:
                raise Exception(f"Ошибка при создании платежа: {response.status}")


BASE_API_URL = "https://vpnbot.onrender.com/payments/api/crypto/create/"  # вставь сюда свой домен


async def create_crypto_payment(telegram_id: int, amount: int):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            BASE_API_URL,
            json={"telegram_id": telegram_id, "amount": amount},
            timeout=10
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("payment_url")
            else:
                data = await response.json()
                raise Exception(data.get("error", "Не удалось создать платёж"))