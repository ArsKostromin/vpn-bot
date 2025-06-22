from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



get_support_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="поддержка", url="https://t.me/Anonixvpnsupportbot"),
        ],
    ]
)

get_main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Главное меню", callback_data="start_from_button"),
        ],
    ]
)