from aiohttp import web

routes = web.RouteTableDef()

@routes.post("/notify")
async def notify_handler(request):
    try:
        data = await request.json()
        tg_id = data["tg_id"]
        amount = data["amount"]
        payment_id = data.get("payment_id")

        message = f"✅ Оплата на {amount}₽ прошла успешно!\nID платежа: {payment_id}"

        # получаем бот из контекста
        bot = request.app["bot"]
        await bot.send_message(tg_id, message)

        return web.json_response({"status": "ok"})

    except Exception as e:
        print(f"[!] Ошибка в notify_handler: {e}")
        return web.json_response({"error": str(e)}, status=500)

async def run_aiohttp_server(bot_instance):
    app = web.Application()
    app["bot"] = bot_instance  # передаём бота в контекст
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)  # слушаем на 8080
    await site.start()
    print("[i] AIOHTTP сервер запущен на порту 8080")
