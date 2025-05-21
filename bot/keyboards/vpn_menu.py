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
    # Карта для преобразования суффикса в слово
    suffix_map = {
        'm': 'месяц',
        'y': 'год',
    }

    def format_duration(code: str) -> str:
        num = code[:-1]
        suffix = code[-1]
        word = suffix_map.get(suffix, '')
        # Простое склонение (можно улучшить при необходимости)
        if word == 'месяц':
            word = 'месяц' if num == '1' else 'месяца' if num in ['2', '3', '4'] else 'месяцев'
        elif word == 'год':
            word = 'год' if num == '1' else 'года' if num in ['2', '3', '4'] else 'лет'
        return f"{num} {word}"

    buttons = [
        [InlineKeyboardButton(
            text=f"{format_duration(duration)} — Р{price}",
            callback_data=f"duration:{duration}"
        )]
        for duration, price in durations_with_price
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
