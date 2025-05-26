# keyboards/vpn_menu.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_vpn_type_kb(types: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for value, display in types:
        kb.button(text=display, callback_data=f"vpn_type:{value}")
    kb.button(text="⬅️ Назад", callback_data="start_from_button")
    kb.adjust(2)
    return kb.as_markup()


def get_duration_kb(durations: list[tuple[str, str, str, int]]) -> InlineKeyboardMarkup:
    buttons = []

    for code, price, display, discount_percent in durations:
        if discount_percent > 0:
            price = float(price)
            discount_price = price * (1 - discount_percent / 100)
            text = f"{display} — ~{price:.2f}$~ {discount_price:.2f}$ 🔥"
        else:
            text = f"{display} — {price}$"

        buttons.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"duration:{code}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(text="⬅️ Назад", callback_data="start_from_button")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_insufficient_funds_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="balance_up")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="buy_vpn")]
    ])


get_instruktion_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Инструкция", url="http://159.198.77.222:8080/"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="start_from_button"),
        ],
    ]
)


get_target_vpn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🌭 Для YouTube и соцсетей", callback_data="target:social"),
        ],
        [
            InlineKeyboardButton(text="🏴‍☠️ Для торрентов", callback_data="target:torrent"),
        ],
        [
            InlineKeyboardButton(text="🛡 Двойное шифрование (Double VPN)", callback_data="target:double"),
        ],
        [
            InlineKeyboardButton(text="🌐 Выбор по стране", callback_data="country"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="start_from_button"),
        ],
    ]
)


def get_country_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🇺🇸 США", callback_data="target_country"),
            InlineKeyboardButton(text="🇧🇷 Бразилия", callback_data="target_country")
        ],
        [
            InlineKeyboardButton(text="🇩🇪 Германия", callback_data="target_country"),
            InlineKeyboardButton(text="🇯🇵 Япония", callback_data="target_country")
        ],
        [
            InlineKeyboardButton(text="🇦🇪 ОАЭ", callback_data="target_country"),
            InlineKeyboardButton(text="🇦🇺 Австралия", callback_data="target_country")
        ],
        [
            InlineKeyboardButton(text="🇷🇺 Россия", callback_data="target_country"),
            InlineKeyboardButton(text="🇿🇦 ЮАР", callback_data="target_country")
        ],
        [
            InlineKeyboardButton(text="⚙️ Аккаунт", callback_data="account")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="start_from_button")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)