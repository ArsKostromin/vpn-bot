import logging
from aiohttp import web
from bot.keyboards.notify_meny import get_support_kb, get_main_menu_kb
from bot.handlers.balance import robokassa_payment_success
from aiogram.fsm.context import FSMContext, StorageKey

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
        logger.info(f"[NOTIFY] Получены данные: {data}")
        notification_type = data.get("type", "payment")

        bot = request.app["bot"]

        if notification_type == "notification":
            tg_ids = data.get("tg_ids")
            message = data.get("message", "Уведомление")
            image_url = data.get("image_url")
            logger.info(f"[NOTIFY] Итоговый image_url: {image_url}")
            if not tg_ids or not isinstance(tg_ids, list):
                logger.error("[NOTIFY] tg_ids должен быть списком")
                return web.json_response({"error": "tg_ids должен быть списком"}, status=400)
            for tg_id in tg_ids:
                try:
                    if image_url:
                        if isinstance(image_url, str) and image_url.startswith("http"):
                            await bot.send_photo(tg_id, image_url, caption=message)
                            logger.info(f"[NOTIFY] Фото успешно отправлено пользователю {tg_id}: {image_url}")
                        else:
                            logger.warning(f"[NOTIFY] Некорректный image_url для пользователя {tg_id}: {image_url}. Отправляю только текст.")
                            await bot.send_message(tg_id, message)
                            logger.info(f"[NOTIFY] Текст успешно отправлен пользователю {tg_id} (без фото)")
                    else:
                        await bot.send_message(tg_id, message)
                        logger.info(f"[NOTIFY] Текст успешно отправлен пользователю {tg_id} (без фото)")
                except Exception as e:
                    logger.error(f"[NOTIFY] Ошибка отправки пользователю {tg_id}: {e}", exc_info=True)
            return web.json_response({"status": "ok"})

        # --- старые типы ---
        tg_id = data.get("tg_id")
        if notification_type == "payment":
            amount = data["amount"]
            payment_id = data.get("payment_id")
            message = f"✅ Оплата на {amount}$ прошла успешно!\nID платежа: {payment_id}"
            reply_markup = None
        elif notification_type == "ban_notification":
            message = data["message"]
            reply_markup = get_support_kb
        elif notification_type == "unban_notification":
            message = data["message"]
            reply_markup = get_main_menu_kb
        else:
            message = data.get("message", "Уведомление")
            reply_markup = None

        if tg_id:
            # Для успешной оплаты Робокассы вызываем возврат на оплату VPN
            fsm_context = FSMContext(
                storage=bot.dispatcher.storage,
                key=StorageKey(
                    chat_id=tg_id,
                    user_id=tg_id,
                    bot_id=bot.id
                )
            )
            sent_message = await bot.send_message(tg_id, message, reply_markup=reply_markup)
            await robokassa_payment_success(sent_message, fsm_context)
            logger.info(f"[NOTIFY] Отправлено сообщение пользователю {tg_id} типа {notification_type} и вызван возврат на оплату VPN")

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