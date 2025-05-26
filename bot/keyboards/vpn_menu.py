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


def get_duration_kb(plans: list[tuple[str, str, str, int]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for duration_code, price, label, discount_percent, discount_price in plans:
        btn_text = f"{label} – {discount_price}$"
        if discount_percent and int(discount_percent) > 0:
            btn_text += f" 🔻{discount_percent}%"

        builder.button(
            text=btn_text,
            callback_data=f"duration:{duration_code}"
        )

    builder.adjust(2)  # <-- ключевой момент: группирует по 2 в ряд
    return builder.as_markup()


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

def get_confirmation_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Оплатить", callback_data="confirm_payment")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="start_from_button")],
    ])