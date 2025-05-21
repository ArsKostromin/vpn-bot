# services/buy_vpn.py

import httpx

API_URL = "https://server2.anonixvpn.space/vpn"
# API_URL = "http://backend:8000/vpn"


async def get_vpn_types_from_api() -> list[tuple[str, str]]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/plans/")
        response.raise_for_status()
        plans = response.json()
        # Собираем пары (vpn_type, vpn_type_display) и удаляем дубли
        unique_types = {(plan['vpn_type'], plan['vpn_type_display']) for plan in plans}
        return list(unique_types)


async def get_durations_by_type_from_api(vpn_type: str) -> list[tuple[str, str, str]]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/plans/")
        response.raise_for_status()
        plans = response.json()
        return [
            (p['duration'], p['price'], p['duration_display'])
            for p in plans
            if p['vpn_type'] == vpn_type
        ]


async def buy_subscription_api(telegram_id: int, vpn_type: str, duration: str) -> tuple[bool, str, str | None]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/plans/")
        response.raise_for_status()
        plans = response.json()

        matching = [p for p in plans if p['vpn_type'] == vpn_type and p['duration'] == duration]
        if not matching:
            return False, "Такого тарифа не существует.", None
        
        plan_id = matching[0]['id']
        buy_resp = await client.post(
            f"{API_URL}/buy/",
            json={"plan_id": plan_id, "telegram_id": telegram_id}
        )

        if buy_resp.status_code == 201:
            data = buy_resp.json()
            return True, data.get("message", "Подписка успешно оформлена."), data.get("vless")
        else:
            try:
                error_data = buy_resp.json()
                return False, error_data.get("error") or error_data.get("detail", "недостаточно средств"), None
            except Exception:
                return False, f"Ошибка сервера ({buy_resp.status_code})", None
