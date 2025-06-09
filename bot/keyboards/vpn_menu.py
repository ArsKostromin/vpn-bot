# keyboards/vpn_menu.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.services.vless_countries import VLESS_COUNTRY_MAP


def get_vpn_type_kb(types: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for value, display in types:
        kb.button(text=display, callback_data=f"vpn_type:{value}")
    kb.button(text="⬅️ Назад", callback_data="start_from_button")
    kb.adjust(2)
    return kb.as_markup()


def get_duration_kb(durations: list[tuple[str, str, str, int]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for code, price, display, discount_percent in durations:
        price = float(price)
        if discount_percent > 0:
            discount_price = price * (1 - discount_percent / 100)
            text = f"{display} — {price:.2f}$ ~ {discount_price:.2f}$"
        else:
            text = f"{display} — {price:.2f}$"

        builder.button(text=text, callback_data=f"duration:{code}")
    builder.button(text="⬅️ Назад", callback_data="start_from_button")
    builder.adjust(2)
    return builder.as_markup()


def get_insufficient_funds_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="balance_up")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="buy_vpn")]
    ])


def get_instruktion_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Инструкция", url="http://159.198.77.222:8080/")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="start_from_button")]
    ])


def get_country_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for emoji_name in VLESS_COUNTRY_MAP.keys():
        code = emoji_name.encode("utf-8").hex()
        builder.button(text=emoji_name, callback_data=f"vless_country:{code}")
    builder.button(text="⬅️ Назад", callback_data="start_from_button")
    builder.adjust(2)
    return builder.as_markup()


def get_confirmation_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Оплатить", callback_data="confirm_payment")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="start_from_button")],
    ])
