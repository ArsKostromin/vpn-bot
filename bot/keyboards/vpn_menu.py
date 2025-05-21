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


def get_duration_kb(durations: list[tuple[str, str, str]]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(
            text=f"{display} — Р{price}",
            callback_data=f"duration:{code}"
        )]
        for code, price, display in durations
    ]

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
            InlineKeyboardButton(text="🏴‍☠️ Для торрентов", callback_data="target:torrent"),  # пока такой же
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
            InlineKeyboardButton(text="🇺🇸 США", callback_data="target:usa"),
            InlineKeyboardButton(text="🇧🇷 Бразилия", callback_data="target:brazil")
        ],
        [
            InlineKeyboardButton(text="🇩🇪 Германия", callback_data="target:germany"),
            InlineKeyboardButton(text="🇯🇵 Япония", callback_data="target:japan")
        ],
        [
            InlineKeyboardButton(text="🇦🇪 ОАЭ", callback_data="target:uae"),
            InlineKeyboardButton(text="🇦🇺 Австралия", callback_data="target:australia")
        ],
        [
            InlineKeyboardButton(text="🇷🇺 Россия", callback_data="target:russia"),
            InlineKeyboardButton(text="🇿🇦 ЮАР", callback_data="target:southafrica")
        ],
        [
            InlineKeyboardButton(text="⚙️ Аккаунт", callback_data="account")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="start_from_button")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
