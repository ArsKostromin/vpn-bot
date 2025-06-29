# bot/keyboards/inline_main_menu.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛡 Начать пользоваться", callback_data="buy_vpn"),
        ],
        [
            InlineKeyboardButton(text="💳 Пополнить", callback_data="balance_up"),
            InlineKeyboardButton(text="⚙️ Аккаунт", callback_data="account"),
        ],
        [
            InlineKeyboardButton(text="📦 Мои услуги", callback_data="my_services"),
            InlineKeyboardButton(text="🎁 Промокоды", callback_data="coupon"),
            
        ],
        [
            
            InlineKeyboardButton(text="🤝 Как подключить", url="https://arskostromin.github.io/vpnguide/index.html"),
            InlineKeyboardButton(text="🆘 Помощь", url="https://t.me/Anonixvpnsupportbot")
        ],
        [
            InlineKeyboardButton(text="ℹ️ О нас", callback_data="about_us"),
        ],
    ]
)


inline_buyvpn_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛡 для ютуба и соцсетей", callback_data="for_youtube"),
        ],
        [
            InlineKeyboardButton(text="📦для торрентов", callback_data="for_torrent"),
        ],
        [
            InlineKeyboardButton(text="💳 выбор по стране", callback_data="by_country"),
        ],
        [
            InlineKeyboardButton(text="🔙 назад", callback_data="back_to_main"),
        ],
    ]
)


inline_time_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1 мес", callback_data="for_youtube"),
            InlineKeyboardButton(text="2 мес", callback_data="for_youtube"),
        ],
        [
            InlineKeyboardButton(text="1 год", callback_data="for_youtube"),
            InlineKeyboardButton(text="3 года", callback_data="for_youtube"),        
        ],
        [
            InlineKeyboardButton(text="назад", callback_data="back"),
        ],
    ]
)

inline_country_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1 страна", callback_data="for_youtube"),
            InlineKeyboardButton(text="2 страна", callback_data="for_youtube"),
        ],
        [
            InlineKeyboardButton(text="1 страна", callback_data="for_youtube"),
            InlineKeyboardButton(text="3 страна", callback_data="for_youtube"),        
        ],
        [
            InlineKeyboardButton(text="назад", callback_data="back"),
        ],
    ]
)


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_target_vpn() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔒 Соцсети", callback_data="vpn_type:social")],
        [InlineKeyboardButton(text="🎬 Стриминг", callback_data="vpn_type:stream")],
        [InlineKeyboardButton(text="⚙️ Выбрать по стране", callback_data="country")]
    ])
    return keyboard


def get_country_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Россия", callback_data="vpn_type:ru")],
        [InlineKeyboardButton(text="🇺🇸 США", callback_data="vpn_type:us")],
        [InlineKeyboardButton(text="🇳🇱 Нидерланды", callback_data="vpn_type:nl")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ])
    return keyboard
