import aiohttp

async def register_user_via_api(telegram_id: int) -> str | None:
    url = "http://backend:8000/user/api/register/"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"telegram_id": telegram_id}) as resp:
            text = await resp.text()
            if resp.status == 201:
                try:
                    data = await resp.json()
                    vpn_key = data.get("vpn_key")
                    created = data.get("created")
                    return vpn_key, created
                except Exception as e:
                    print(f"Ошибка парсинга JSON: {e}, ответ: {text}")
                    return None
            else:
                print(f"[❌] Ошибка регистрации: статус={resp.status}, тело={text}")
                return None
