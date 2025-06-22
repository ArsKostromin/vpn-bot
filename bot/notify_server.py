import logging
from aiohttp import web

# 🔧 Настрой логгер
logger = logging.getLogger("aiohttp_notify")
logger.setLevel(logging.INFO)

# Можно писать в файл или консоль
handler = logging.StreamHandler()  # лог в stdout
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

routes = web.RouteTableDef()


@routes.post("/notify")
async def notify_handler(request):
    try:
        data = await request.json()
        tg_id = data["tg_id"]
        
        # Определяем тип уведомления
        notification_type = data.get("type", "payment")
        
        if notification_type == "payment":
            # Старое уведомление о платеже
            amount = data["amount"]
            payment_id = data.get("payment_id")
            message = f"✅ Оплата на {amount}$ прошла успешно!\nID платежа: {payment_id}"
        elif notification_type == "ban_notification":
            # Уведомление о бане
            message = data["message"]
        elif notification_type == "unban_notification":
            # Уведомление о разбане
            message = data["message"]
        else:
            # По умолчанию используем message из данных
            message = data.get("message", "Уведомление")

        bot = request.app["bot"]
        await bot.send_message(tg_id, message)

        logger.info(f"[NOTIFY] Отправлено сообщение пользователю {tg_id} типа {notification_type}")

        return web.json_response({"status": "ok"})

    except Exception as e:
        logger.exception(f"[NOTIFY] Ошибка обработки запроса: {e}")
        return web.json_response({"error": str(e)}, status=500)


async def run_aiohttp_server(bot_instance):
    app = web.Application()
    app["bot"] = bot_instance
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8081)  # 👈 порт должен совпадать с тем, что указан в docker-compose
    await site.start()

    logger.info("[SERVER] AIOHTTP сервер запущен на порту 8081")