# services/buy_vpn.py

import httpx

API_URL = "http://backend:8000/vpn"  # заменишь на свой адрес

async def get_vpn_types_from_api() -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/plans/")
        response.raise_for_status()
        plans = response.json()
        return list(set(plan['vpn_type'] for plan in plans))

async def get_durations_by_type_from_api(vpn_type: str) -> list[tuple[str, str]]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/plans/")
        response.raise_for_status()
        plans = response.json()
        return [(p['duration'], p['price']) for p in plans if p['vpn_type'] == vpn_type]


async def buy_subscription_api(telegram_id: int, vpn_type: str, duration: str) -> tuple[bool, str]:
    async with httpx.AsyncClient() as client:
        # Получаем список тарифов
        response = await client.get(f"{API_URL}/plans/")
        response.raise_for_status()
        plans = response.json()

        # Находим подходящий тариф
        matching = [p for p in plans if p['vpn_type'] == vpn_type and p['duration'] == duration]
        if not matching:
            return False, "Такого тарифа не существует."
        
        plan_id = matching[0]['id']
        buy_resp = await client.post(
            f"{API_URL}/buy/",
            json={"plan_id": plan_id, "telegram_id": telegram_id}  # 👈 Добавили telegram_id
        )

        if buy_resp.status_code == 201:
            return True, buy_resp.json()['message']
        else:
            # Если ошибка — пробуем показать её, иначе выводим общее сообщение
            return False, buy_resp.json().get("error") or buy_resp.json().get("detail", "Ошибка при покупке.")
        
        
# async def get_price_by_plan(vpn_type: str) -> list[str]:
#     async with httpx.AsyncClient() as client:
#         response = await client.get(f"{API_URL}/plans/")
#         response.raise_for_status()
#         plans = response.json()
#         return [p['price'] for p in plans if p['vpn_type'] == vpn_type]