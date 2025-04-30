#services/upbalance.py
import aiohttp

API_URL = "http://159.198.77.150:8000"  # У тебя в докере так
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


#крипта
async def create_crypto_payment(telegram_id: int, amount: int, asset: str = "TON"):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"{API_URL}/payments/api/crypto/create/",
            json={"telegram_id": telegram_id, "amount": amount, "asset": asset},
            timeout=10
        ) as response:
            data = await response.json()
            if response.status == 200:
                return data.get("payment_url")
            raise Exception(data.get("error", "Не удалось создать платёж"))
