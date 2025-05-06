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
            InlineKeyboardButton(text="🏴‍☠️ Для торрентов", callback_data="buy_vpn1"),  # можно позже сделать `target:torrent`
        ],
        [
            InlineKeyboardButton(text="🌐 Выбор по стране", callback_data="country"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="start_from_button"),
        ],
    ]
)



from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_country_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🇬🇧 Британия", callback_data="buy_vpn1"),
            InlineKeyboardButton(text="🇩🇪 Германия", callback_data="buy_vpn1")
        ],
        [
            InlineKeyboardButton(text="🇮🇱 Израиль", callback_data="buy_vpn1"),
            InlineKeyboardButton(text="🇪🇸 Испания", callback_data="buy_vpn1")
        ],
        [
            InlineKeyboardButton(text="🇰🇿 Казахстан", callback_data="buy_vpn1"),
            InlineKeyboardButton(text="🇨🇦 Канада", callback_data="buy_vpn1")
        ],
        [
            InlineKeyboardButton(text="🇳🇱 Нидерланды", callback_data="buy_vpn1"),
            InlineKeyboardButton(text="🇦🇪 ОАЭ", callback_data="buy_vpn1")
        ],
        [
            InlineKeyboardButton(text="🇵🇱 Польша", callback_data="buy_vpn1"),
            InlineKeyboardButton(text="🇷🇺 Россия", callback_data="buy_vpn1")
        ],
        [
            InlineKeyboardButton(text="🇺🇸 США", callback_data="buy_vpn1"),
            InlineKeyboardButton(text="🇹🇷 Турция", callback_data="buy_vpn1")
        ],
        [
            InlineKeyboardButton(text="🇺🇦 Украина", callback_data="buy_vpn1"),
            InlineKeyboardButton(text="🇫🇷 Франция", callback_data="buy_vpn1")
        ],
        [
            InlineKeyboardButton(text="🇸🇪 Швеция", callback_data="buy_vpn1"),
            InlineKeyboardButton(text="🇯🇵 Япония", callback_data="buy_vpn1")
        ],
        [
            InlineKeyboardButton(text="⚙️ Аккаунт", callback_data="account")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="start_from_button")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
