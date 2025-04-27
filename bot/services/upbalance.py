import aiohttp

API_URL = "http://backend:8000"  # У тебя в докере так

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
