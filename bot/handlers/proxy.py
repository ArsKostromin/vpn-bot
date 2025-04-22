from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramBadRequest
from bot.keyboards.proxy_menu import proxy_service_menu, buy_proxy_keyboard
from .start import process_start 

router = Router()


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await process_start(callback.from_user.id, callback.from_user.username, callback.message)
    await callback.answer()

    
@router.callback_query(F.data.in_({"buy_proxy", "back_proxy"}))
async def show_buy_proxy(callback: CallbackQuery):
    await proxy_screen(callback)
    
    
async def proxy_screen(callback: CallbackQuery):
    """Отображает стартовый экран выбора proxy."""
    try:
        await callback.bot.send_photo(
            chat_id=callback.message.chat.id,
            photo="https://play-lh.googleusercontent.com/BFkf2bgtxsCvsTnR2yw8yuWD3mgpThoyiRoBhoazTqFFMNOmdxGAAqS7vMATyNwelQ",
            caption=(
                "🛡️ <b>YouFast™ Proxy</b>\n\n"
                "👉 Получите первоклассные чистые прокси под любые ваши нужды в нашем удобном боте.\n\n"
                "В настоящее время вы можете приобрести:\n\n"
                "📲 <b>Мобильные прокси</b> (используют IP-адреса мобильных операторов)\n"
                "🏠 <b>Резидентские прокси</b> (IP-адреса обычных домашних пользователей, то есть с роутеров)\n\n"
                "-----------------------------\n"
                "Выберите VPN по цели использования или стране ⬇️\n\n"
                "⚠️ Вы получите VPN той страны, в которой мы гарантируем работу выбранного вами направления.\n\n"
                "Если же вам нужна конкретная страна VPN – жмите «Выбрать по стране»."
            ),
            reply_markup=proxy_service_menu,
            parse_mode="HTML"
        )
    except TelegramBadRequest:
        await callback.message.answer("Произошла ошибка при обработке запроса.")

@router.callback_query(F.data == "buy_proxy2")
async def buy_proxy_screen(callback: CallbackQuery):
    photo = FSInputFile("bot/media/telegram.jpg")
    await callback.message.answer_photo(
        photo=photo,
        caption=(
            "🛡️ <b>YouFast™ Proxy</b>\n\n"
            "<b>📲 Мобильные</b> – прокси сотовых операторов. Используются для самых чувствительных целей.\n\n"
            "<b>🏠 Резидентские</b> – IP-адреса реальных домашних роутеров. Высокая скорость и стабильность.\n\n"
            "<b>🔁 Резидентские с ротацией</b> – Динамический IP-адрес меняется, доступны все страны.\n\n"
            "<b>Какой тип прокси вас интересует?</b>"
        ),
        reply_markup=buy_proxy_keyboard
    )
    await callback.answer()