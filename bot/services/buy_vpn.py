# services/buy_vpn.py
import httpx

API_URL = "https://server2.anonixvpn.space/vpn"
# API_URL = "http://backend:8000/vpn"


async def get_vpn_types_from_api() -> list[tuple[str, str]]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/plans/")
        response.raise_for_status()
        plans = response.json()
        unique_types = {(plan['vpn_type'], plan['vpn_type_display']) for plan in plans}
        return list(unique_types)


async def get_durations_by_type_from_api(vpn_type: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/plans/")
        response.raise_for_status()
        plans = response.json()
        return [
            {
                "duration": p["duration"],
                "duration_display": p["duration_display"],
                "price": float(p["price"]),
                "discount_active": p["discount_active"],
                "discount_percent": p.get("discount_percent", 0),
                "discount_price": float(p["discount_price"]) if p["discount_price"] else None,
            }
            for p in plans
            if p['vpn_type'] == vpn_type
        ]



import httpx
import logging

logger = logging.getLogger(__name__)

async def buy_subscription_api(
    telegram_id: int,
    vpn_type: str,
    duration: str,
    country: str = None
) -> tuple[bool, str, str | None]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/plans/")
            response.raise_for_status()
            plans = response.json()

            logger.info("📦 Получены тарифы: %s", plans)
            logger.info("🔍 Ищем vpn_type=%s, duration=%s, country=%s", vpn_type, duration, country)

            matching = [
                p for p in plans
                if p['vpn_type'] == vpn_type and p['duration'] == duration
                   and (vpn_type != "country" or p.get("country", "").lower() == (country or "").lower())
            ]

            if not matching:
                logger.warning("❌ Подходящий тариф не найден! Доступные планы: %s", plans)
                return False, "Такого тарифа не существует.", None

            plan_id = matching[0]['id']
            logger.info("✅ Найден тариф id=%s", plan_id)

            buy_resp = await client.post(
                f"{API_URL}/buy/",
                json={"plan_id": plan_id, "telegram_id": telegram_id}
            )

            if buy_resp.status_code == 201:
                data = buy_resp.json()
                logger.info("🎉 Подписка оформлена: %s", data)
                return True, data.get("message", "Подписка успешно оформлена."), data.get("vless")
            else:
                try:
                    error_data = buy_resp.json()
                    logger.error("💥 Ошибка при оформлении: %s", error_data)
                    return False, error_data.get("error") or error_data.get("detail", "недостаточно средств"), None
                except Exception as e:
                    logger.exception("💣 Ошибка при разборе ошибки: %s", e)
                    return False, f"Ошибка сервера ({buy_resp.status_code})", None

    except Exception as e:
        logger.exception("🔥 Общая ошибка в buy_subscription_api: %s", e)
        return False, "Внутренняя ошибка сервера", None




def build_tariff_showcase(title: str, plans: list[dict]) -> str:
    lines = [f"🤳 {title}", "", "💰 *Лучший VPN по лучшей цене!*", ""]

    for plan in plans:
        base_price = plan["price"]
        discount_price = plan.get("discount_price")
        percent = plan.get("discount_percent", 0)
        label = plan["duration_display"]

        if discount_price and percent > 0:
            lines.append(f"├ {label}: ${discount_price:.2f} (-{percent}%)")
        else:
            lines.append(f"├ {label}: ${base_price:.2f}")

    return "\n".join(lines)

async def get_countries_from_api() -> list[tuple[str, str]]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/countries/")
        response.raise_for_status()
        countries = response.json()
        unique_types = {(item['name'], item['country']) for item in countries}
        return list(unique_types)