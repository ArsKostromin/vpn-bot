from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from bot.keyboards.vpn_menu import inline_buyvpn_menu, inline_time_menu, inline_country_menu
from .start import process_start 

router = Router()


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await process_start(callback.from_user.id, callback.from_user.username, callback.message)
    await callback.answer()

    
@router.callback_query(F.data.in_({"buy_vpn", "back"}))
async def show_buy_vpn(callback: CallbackQuery):
    await buy_vpn_screen(callback)    
    
    
async def buy_vpn_screen(callback: CallbackQuery):
    """Отображает стартовый экран выбора VPN."""
    try:
        await callback.bot.send_photo(
            chat_id=callback.message.chat.id,
            photo="https://play-lh.googleusercontent.com/BFkf2bgtxsCvsTnR2yw8yuWD3mgpThoyiRoBhoazTqFFMNOmdxGAAqS7vMATyNwelQ",
            caption=(
                "Выберите VPN по цели использования или стране ⬇️\n\n"
                "⚠️ Вы получите VPN той страны, в которой мы гарантируем работу выбранного вами направления.\n\n"
                "Если же вам нужна конкретная страна VPN – жмите «Выбрать по стране»."
            ),
            reply_markup=inline_buyvpn_menu,
            parse_mode="HTML"
        )
    except TelegramBadRequest:
        await callback.message.answer("Произошла ошибка при обработке запроса.")


@router.callback_query(F.data == "for_youtube")
async def vpn_for_youtube(callback: CallbackQuery):
    try:
        await callback.bot.send_photo(
            chat_id=callback.message.chat.id,
            photo="https://play-lh.googleusercontent.com/BFkf2bgtxsCvsTnR2yw8yuWD3mgpThoyiRoBhoazTqFFMNOmdxGAAqS7vMATyNwelQ",
            caption=(
                "🤳 Для YouTube и соцсетей\n\n"
                "💰 Лучший VPN по лучшей цене!\n\n"
                "├ 1 мес: $5\n"
                "├ 6 мес: $27.0 (-10%)\n"
                "├ 1 год: $48.7 (-20%)\n"
                "├ 3 года: $109.5 (-40%)\n\n"
                "Если же вам нужна конкретная страна VPN – жмите «Выбрать по стране»."
            ),
            reply_markup=inline_time_menu,
            parse_mode="HTML"
        )
    except TelegramBadRequest:
        await callback.message.answer("Произошла ошибка при обработке запроса.")


@router.callback_query(F.data == "for_torrent")
async def vpn_for_torrent(callback: CallbackQuery):
    try:
        await callback.bot.send_photo(
            chat_id=callback.message.chat.id,
            photo="https://play-lh.googleusercontent.com/BFkf2bgtxsCvsTnR2yw8yuWD3mgpThoyiRoBhoazTqFFMNOmdxGAAqS7vMATyNwelQ",
            caption=(
                "🏴‍☠️ Для торрентов\n\n"
                "💰 Лучший VPN по лучшей цене!\n\n"
                "├ 1 мес: $5\n"
                "├ 6 мес: $27.0 (-10%)\n"
                "├ 1 год: $48.7 (-20%)\n"
                "├ 3 года: $109.5 (-40%)\n\n"
                "Если же вам нужна конкретная страна VPN – жмите «Выбрать по стране»."
            ),
            reply_markup=inline_time_menu,
            parse_mode="HTML"
        )
    except TelegramBadRequest:
        await callback.message.answer("Произошла ошибка при обработке запроса.")


@router.callback_query(F.data == "by_country")
async def vpn_by_country(callback: CallbackQuery):
    try:
        await callback.bot.send_photo(
            chat_id=callback.message.chat.id,
            photo="https://play-lh.googleusercontent.com/BFkf2bgtxsCvsTnR2yw8yuWD3mgpThoyiRoBhoazTqFFMNOmdxGAAqS7vMATyNwelQ",
            caption=(
                "Выберите страну для вашего VPN ⬇️\n\n"
                "⚠️ Если вам нужен VPN для соцсетей или торрентов – вернитесь назад и выберите цель использования. "
                "Ни в коем случае не используйте просто страновой VPN для скачивания с торрентов!\n\n"
                "⛔️ Выбирая страну самостоятельно, мы НЕ гарантируем что ваш инстаграм будет работать в России с российского IP 😄"
            ),
            reply_markup=inline_country_menu,
            parse_mode="HTML"
        )
    except TelegramBadRequest:
        await callback.message.answer("Произошла ошибка при обработке запроса.")



@router.callback_query(F.data == "account")
async def account(callback: CallbackQuery):
    await callback.message.answer("📦 Здесь будут наши услуги")
    await callback.answer()

@router.callback_query(F.data == "top_up")
async def top_up(callback: CallbackQuery):
    await callback.message.answer("📦 Здесь будут наши услуги")
    await callback.answer()

@router.callback_query(F.data == "help")
async def help_handler(callback: CallbackQuery):
    await callback.message.answer("📦 Здесь будут наши услуги")
    await callback.answer()

@router.callback_query(F.data == "reviews")
async def reviews(callback: CallbackQuery):
    await callback.message.edit_text("✍️ Здесь будут отзывы")
    await callback.answer()

@router.callback_query(F.data == "about_us")
async def about_us(callback: CallbackQuery):
    await callback.message.answer("📦 Здесь будут наши услуги")
    await callback.answer()

@router.callback_query(F.data == "gift_friend")
async def gift_friend(callback: CallbackQuery):
    await callback.message.answer("📦 Здесь будут наши услуги")
    await callback.answer()

@router.callback_query(F.data == "partners")
async def partners(callback: CallbackQuery):
    await callback.message.answer("📦 Здесь будут наши услуги")
    await callback.answer()

@router.callback_query(F.data == "other_services")
async def other_services(callback: CallbackQuery):
    await callback.message.answer("📦 Здесь будут наши услуги")
    await callback.answer()
