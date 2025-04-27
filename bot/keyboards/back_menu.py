from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_to_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="start_from_button"),
        ],

    ]
)