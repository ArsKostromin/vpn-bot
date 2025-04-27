# keyboards/vpn_menu.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_vpn_type_kb(types: list[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for vpn_type in types:
        kb.button(text=vpn_type, callback_data=f"vpn_type:{vpn_type}")
    kb.button(text="⬅️ Назад", callback_data="start_from_button")  # добавляем кнопку Назад
    kb.adjust(2)  # 2 кнопки в ряд
    return kb.as_markup()

def get_duration_kb(durations_with_price: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"{duration} — Р{price}", callback_data=f"duration:{duration}")]
        for duration, price in durations_with_price
    ]
    # Добавляем кнопку Назад отдельным рядом
    buttons.append(
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="start_from_button")]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)