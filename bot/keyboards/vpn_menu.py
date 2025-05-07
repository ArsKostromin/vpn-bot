# keyboards/vpn_menu.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Все цели VPN (используется и в handler'е)
TARGETS = {
    "social": "🌭 Для YouTube и соцсетей",
    "torrent": "🏴‍☠️ Для торрентов",
    "double": "🛡 Двойное шифрование (Double VPN)",
    "country": "🌐 Выбор по стране",
}

# VPN-тип
def get_vpn_type_kb(types: list[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for vpn_type in types:
        kb.button(text=vpn_type, callback_data=f"vpn_type:{vpn_type}")
    kb.button(text="⬅️ Назад", callback_data="start_from_button")
    kb.adjust(2)
    return kb.as_markup()


# Продолжительность
def get_duration_kb(durations_with_price: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"{duration} — Р{price}", callback_data=f"duration:{duration}")]
        for duration, price in durations_with_price
    ]
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="start_from_button")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Недостаточно средств
def get_insufficient_funds_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="balance_up")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="buy_vpn")]
    ])


# Инструкция
get_instruktion_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Инструкция", url="http://159.198.77.222:8080/")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="start_from_button")],
    ]
)


# Выбор цели VPN
def get_target_vpn_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"target:{key}")]
        for key, label in TARGETS.items()
    ]
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="start_from_button")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Выбор страны
def get_country_kb() -> InlineKeyboardMarkup:
    countries = [
        ("🇬🇧 Британия", "🇩🇪 Германия"),
        ("🇮🇱 Израиль", "🇪🇸 Испания"),
        ("🇰🇿 Казахстан", "🇨🇦 Канада"),
        ("🇳🇱 Нидерланды", "🇦🇪 ОАЭ"),
        ("🇵🇱 Польша", "🇷🇺 Россия"),
        ("🇺🇸 США", "🇹🇷 Турция"),
        ("🇺🇦 Украина", "🇫🇷 Франция"),
        ("🇸🇪 Швеция", "🇯🇵 Япония"),
    ]
    buttons = [[
        InlineKeyboardButton(text=left, callback_data="target:country"),
        InlineKeyboardButton(text=right, callback_data="target:country")
    ] for left, right in countries]
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="start_from_button")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
