from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_balance_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=" 1 ₽", callback_data="topup_1"),
            InlineKeyboardButton(text="100 ₽", callback_data="topup_100"),
            InlineKeyboardButton(text="500 ₽", callback_data="topup_500"),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="start_from_button")
        ]
    ])
    return keyboard
