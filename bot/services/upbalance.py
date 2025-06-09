#services/upbalance.py
import aiohttp

API_URL = "http://server2.anonixvpn.space"
# API_URL = "http://backend:8000"

#robocassa(робосаса)
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


#telegram stars


STAR_PRICE_RUB = 1.79
STAR_TO_RUB = 1.79 # 1 звезда ≈ 1.79₽


async def register_star_payment(user_id: int, stars: float):
    amount = round(stars * STAR_TO_RUB, 2)

    payload = {
        "user_id": user_id,
        "stars": stars,
        "amount": amount,
        "method": "stars",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/payments/payments/stars/", json=payload) as response:
            return await response.json()
