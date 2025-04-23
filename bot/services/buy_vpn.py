import aiohttp

API_BASE_URL = "http://backend:8000/api/vpn"


async def select_vpn_type(telegram_id: int, vpn_type: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE_URL}/select-type/",
            json={"vpn_type": vpn_type},
            headers={"X-Telegram-ID": str(telegram_id)},
        ) as resp:
            data = await resp.json()
            if resp.status == 200:
                return data["vpn_type"]
            raise Exception(data.get("detail", "Ошибка при выборе типа VPN"))


async def select_duration(telegram_id: int, vpn_type: str, duration: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE_URL}/select-duration/",
            json={"vpn_type": vpn_type, "duration": duration},
            headers={"X-Telegram-ID": str(telegram_id)},
        ) as resp:
            data = await resp.json()
            if resp.status == 200:
                return data["duration"]
            raise Exception(data.get("detail", "Ошибка при выборе длительности"))


async def purchase_subscription(telegram_id: int, vpn_type: str, duration: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE_URL}/purchase/",
            json={"vpn_type": vpn_type, "duration": duration},
            headers={"X-Telegram-ID": str(telegram_id)},
        ) as resp:
            data = await resp.json()
            if resp.status == 201:
                return data
            raise Exception(data.get("detail", "Ошибка при покупке VPN"))
