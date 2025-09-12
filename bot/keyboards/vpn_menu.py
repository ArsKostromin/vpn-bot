# keyboards/vpn_menu.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.services.buy_vpn import get_countries_from_api

def get_vpn_type_kb(types: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for value, display in types:
        kb.button(text=display, callback_data=f"vpn_type:{value}")
    kb.button(text="⬅️ Назад", callback_data="start_from_button")
    kb.adjust(2)
    return kb.as_markup()


def get_duration_kb(durations: list[tuple[str, str, str, int]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    def _rank(item: tuple[str, str, str, int]) -> int:
        code, _, display, _ = item
        code = str(code).lower().strip()
        label = str(display).lower().strip()

        mapping = {
            "1m": 0,
            "3m": 1,
            "6m": 2,
            "12m": 3,
            "1y": 3,
        }
        if code in mapping:
            return mapping[code]

        if "меся" in label:
            if label.startswith("1"):
                return 0
            if label.startswith("3"):
                return 1
            if label.startswith("6"):
                return 2
        if ("год" in label or "года" in label or "лет" in label) and label.startswith("1"):
            return 3
        return 99

    durations_sorted = sorted(durations, key=_rank)

    for code, price, display, discount_percent in durations_sorted:
        if discount_percent > 0:
            price = float(price)
            text = f"{display}—{price:.2f}$"
        else:
            text = f"{display} — {price}$"

        builder.button(
            text=text,
            callback_data=f"duration:{code}"
        )

    builder.button(
        text="⬅️ Назад",
        callback_data="buy_vpn"
    )

    builder.adjust(2)  # вот теперь можно

    return builder.as_markup()


def get_insufficient_funds_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="balance_up")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="buy_vpn")]
    ])


get_instruktion_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Инструкция", url="https://arskostromin.github.io/vpnguide/"),
            InlineKeyboardButton(text="❓ Задать вопрос", url="https://t.me/Anonixvpnsupportbot"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="start_from_button"),
        ],
    ]
)


get_target_vpn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Для YouTube и соцсетей", callback_data="target:social"),
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


async def get_country_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    types = await get_countries_from_api()

    for code, display in types:
        kb.button(text=display, callback_data=f"target_country:{code}")
    kb.button(text="⬅️ Назад", callback_data="buy_vpn")
    kb.adjust(2)
    return kb.as_markup()


def get_confirmation_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Оплатить", callback_data="confirm_payment")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="buy_vpn")],
    ])


