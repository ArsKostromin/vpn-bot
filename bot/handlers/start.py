import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject
from aiogram.enums import ParseMode

from bot.keyboards.main_menu import inline_main_menu
from bot.keyboards.start_menu import inline_instruction_buttons
from bot.keyboards.reply import main_menu_kb
from bot.keyboards.notify_meny import get_support_kb

from bot.services.user_service import register_user_via_api
from bot.services.telegram_service import is_user_subscribed
from bot.services.promo_service import get_promo_code_from_api
from aiogram.types import FSInputFile

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = Router()

@router.message(CommandStart())  # Объединённый хендлер
async def cmd_start(message: Message, command: CommandObject):
    referral_code = command.args if command.args else None
    logger.info(f"Start triggered by {message.from_user.id}, referral: {referral_code}")
    await process_start(message.from_user.id, message.from_user.username, message, referral_code)


@router.message(F.text == "Главное меню")
async def main_menu_button_pressed(message: Message):
    logger.info(f"'Главное меню' button pressed by {message.from_user.id}")
    await process_start(message.from_user.id, message.from_user.username, message)


@router.callback_query(F.data == "start_from_button")
async def callback_start(callback: CallbackQuery):
    logger.info(f"Callback start triggered by {callback.from_user.id}")
    await process_start(callback.from_user.id, callback.from_user.username, callback.message)
    await callback.answer()


async def process_start(
    user_id: int,
    username: str,
    respond_to: Message,
    referral_code: str | None = None
):
    logger.info(f"Processing start for user {user_id} (username: {username}), referral: {referral_code}")
    
    result = await register_user_via_api(user_id, referral_code)
    logger.info(f"User registration result: {result}")

    # Проверяем, забанен ли пользователь
    if isinstance(result, dict) and result.get("error") == "banned":
        ban_reason = result.get("ban_reason", "Причина не указана")
        logger.warning(f"Отправляем сообщение о бане пользователю {user_id}: {ban_reason}")
        await respond_to.answer(
            text=f"🚫 Ваш аккаунт заблокирован\n\nПричина: {ban_reason}\n\nДля разблокировки обратитесь в поддержку.",
            reply_markup=get_support_kb
        )
        logger.info(f"Сообщение о бане отправлено пользователю {user_id}")
        return

    # Показать клавиатуру
    await respond_to.answer(
        text="Меню доступно ниже ⬇️",
        reply_markup=main_menu_kb
    )

    if result:
        link_code, created = result

        if created:
            is_subscribed = await is_user_subscribed(respond_to.bot, user_id)
            logger.info(f"New user {user_id} is subscribed: {is_subscribed}")

            await respond_to.answer(
                text=(
                    f"✅ Добро пожаловать в Anonix, <b>{respond_to.from_user.full_name}</b>!\n\n"
                    "🔧 Ваш VPN УЖЕ готов к работе!\n\n"
                    "🎁 получи <b>+5 дней</b>\n\n"
                    "📢 Чтобы получить <b>бесплатную подписку</b>, подпишитесь на наш канал, нажмите «Проверить подписку», и вы получите промо-код, который нужно будет активировать в главном меню.👇\n\n"
                    "📲 Установите приложение для вашей OS:\n\n"
                    "🍏 iOS: <a href='https://apps.apple.com/ru/app/v2raytun/id6476628951'>Anonix</a>\n"
                    "🤖 Android: <a href='https://play.google.com/store/apps/details?id=app.hiddify.com&hl=ru&pli=1'>Anonix</a>\n"
                    "🖥️ Windows: <a href='https://apps.microsoft.com/detail/9pdfnl3qv2s5?hl=ru-RU&gl=RU'>Anonix</a>\n"
                    "🍏 MacOS: <a href='https://apps.apple.com/ru/app/v2box-v2ray-client/id6446814690'>Anonix</a>\n\n"
                    "🔗 Наш канал:\n\n"
                    "https://t.me/anonix_vpn/"
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=inline_instruction_buttons,
                disable_web_page_preview=True
            )
            return

    # Пользователь уже зарегистрирован
    logger.info(f"User {user_id} already registered")
    await respond_to.bot.send_photo(
        chat_id=respond_to.chat.id,
        photo = FSInputFile("bot/media/anonix.jpg"),
        caption = (
            "🔥 Наш VPN обеспечивает высокую скорость без ограничений — смотрите YouTube в высоком качестве без задержек!\n\n"
            "🛡 Двойное шифрование данных (Double VPN) — ваш трафик под надежным шифрованием.\n\n"
            "🕵️ Полная анонимность — никто не отследит вашу активность.\n\n"
            "💥 Лучшая цена на рынке, не перегружаем сервера ради выгоды!\n\n"
            "✅ Подключайтесь: https://t.me/anonix_vpn"
        ),
        reply_markup=inline_main_menu,
        parse_mode=ParseMode.HTML
    )



@router.callback_query(F.data == "check_subscription")
async def check_subscription_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    logger.info(f"Check subscription for user {user_id}")

    is_subscribed = await is_user_subscribed(callback.bot, user_id)

    if is_subscribed:
        result = await get_promo_code_from_api(user_id)
        promo_code = result.get("promo_code")
        error = result.get("error")
        logger.info(f"User {user_id} subscribed. Promo code: {promo_code}, error: {error}")

        if error:
            await callback.message.answer(
                text=f"❗ {error}",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=main_menu_kb
            )
        else:
            await callback.message.answer(
                text=(
                    "🎉 Спасибо за подписку на канал!\n\n"
                    f"🎁 Вот ваш промокод на +5 дней: `{promo_code}`\n\n"
                    "🚀 Теперь вы можете пользоваться VPN целых 5 дней бесплатно!\n\n"
                    "🎯 Чтобы использовать промокод, вам нужно перейти в главное меню, нажать кнопку 'Промокоды' и ввести выданный промокод"
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=main_menu_kb
            )
    else:
        logger.info(f"User {user_id} has NOT subscribed yet.")
        await callback.message.answer(
            text=(
                "❌ Вы еще не подписались на канал.\n\n"
                "Пожалуйста, подпишитесь и нажмите кнопку ещё раз:" 
                "\n🔗 [Я подписался]()"
            ),
            parse_mode=ParseMode.MARKDOWN
        )

    await callback.answer()



@router.callback_query(F.data == "help")
async def help_handler(callback: CallbackQuery):
    await callback.message.answer("📦 Здесь будут ваши услуги")
    await callback.answer()

@router.callback_query(F.data == "reviews")
async def reviews(callback: CallbackQuery):
    await callback.message.edit_text("✍️ Здесь будут отзывы")
    await callback.answer()

@router.callback_query(F.data == "about_us")
async def about_us(callback: CallbackQuery):
    await callback.message.answer(
        "Представляем вам наш VPN-сервис, который обеспечивает быстрый и безопасный доступ в Интернет благодаря использованию современных протоколов VLESS, Outline с открытым исходным кодом.\n\n"
        "1⃣ Мы применяем SSL для надежного соединения и TLS для шифрования данных, поддерживаем все сетевые протоколы и гарантируем отсутствие утечек. С нами вы можете быть уверены в своей безопасности и конфиденциальности.\n\n"
        "2️⃣ Мы раздаем VPN через Telegram, что делает нас недоступными для блокировок и удаления из магазинов приложений. С Anonix вы всегда на связи, где бы вы ни находились! Это означает, что вы можете легко подключаться к нашему сервису в любой точке мира, не беспокоясь о доступности.\n\n"
        "3️⃣ В отличие от многих бесплатных VPN-сервисов, мы ценим вашу конфиденциальность. Мы не собираем и не продаем ваши данные. Все журналы удаляются с наших серверов мгновенно, а история ваших посещений остается только у вас. После деактивации мы не храним ваши VPN-ключи. Вы можете пользоваться нашим сервисом с полной уверенностью в том, что ваша личная информация защищена.\n\n"
        "4️⃣ Наши сервера обеспечивают неограниченную скорость и трафик (с каналами до 10 Гбит), а наш VPN работает на всех устройствах. Наслаждайтесь просмотром YouTube в 4K без задержек! Кроме того, мы предлагаем простую и интуитивно понятную настройку, чтобы вы могли быстро подключиться к сети без лишних хлопот.\n\n"
        "Выбирая Anonix, вы получаете надежного партнера для безопасного серфинга в Интернете. Присоединяйтесь к нам сегодня и откройте для себя мир без границ!"
    )
    await callback.answer()


@router.callback_query(F.data == "gift_friend")
async def gift_friend(callback: CallbackQuery):
    await callback.message.answer("📦 можно сделать подарок другу")
    await callback.answer()

@router.callback_query(F.data == "partners")
async def partners(callback: CallbackQuery):
    await callback.message.answer("📦 Здесь будут ваши партнеры")
    await callback.answer()

@router.callback_query(F.data == "other_services")
async def other_services(callback: CallbackQuery):
    await callback.message.answer("📦 Здесь будут другие услуги")
    await callback.answer()
    
    
@router.callback_query(F.data == "buy_proxy")
async def buy_proxy(callback: CallbackQuery):
    await callback.message.answer("📦 Здесь будут другие услуги")
    await callback.answer()
