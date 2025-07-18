from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_instruction_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="📥 Инструкция", 
            url="https://arskostromin.github.io/vpnguide/"
        ),
    ],
    [
        InlineKeyboardButton(
            text="Наш канал", 
            url="https://t.me/anonix_vpn/"
        ),
    ],
    [
        InlineKeyboardButton(
            text="🤖 Перейти в бота", 
            callback_data="start_from_button"
        ),
        InlineKeyboardButton(
            text="✅ Я подписался", 
            callback_data="check_subscription"
        ),
    ],
    # [
    #     InlineKeyboardButton(
    #         text="🔗 Показать VPN ключ", 
    #         callback_data="show_vless_key"
    #     ),
    # ]
])



from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Главное меню"),
        ],
    ],
    resize_keyboard=True  # чтобы кнопки аккуратно подстраивались под экран
)
