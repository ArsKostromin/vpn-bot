# keyboards/vpn_menu.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_vpn_type_kb(types: list[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for vpn_type in types:
        kb.button(text=vpn_type, callback_data=f"vpn_type:{vpn_type}")
    kb.adjust(2)  # или 1, 2, 3 — зависит от того, как хочешь выводить кнопки
    return kb.as_markup()


def get_duration_kb(durations_with_price: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"{duration} — ${price}", callback_data=f"duration:{duration}")]
        for duration, price in durations_with_price
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
