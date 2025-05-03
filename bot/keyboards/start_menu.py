from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_instruction_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="📥 Инструкция", 
            url="http://159.198.77.222:8080/"
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
