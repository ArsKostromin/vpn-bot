# bot/keyboards/inline_main_menu.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛡 Купить VPN", callback_data="buy_vpn"),
            InlineKeyboardButton(text="🛒 Купить прокси", callback_data="buy_proxy"),
        ],
        [
            InlineKeyboardButton(text="📦 Мои услуги", callback_data="my_services"),
            InlineKeyboardButton(text="⚙️ Аккаунт", callback_data="account"),
        ],
        [
            InlineKeyboardButton(text="💳 Пополнить", callback_data="balance_up"),
            InlineKeyboardButton(text="🆘 Помощь", callback_data="help"),
        ],
        [
            InlineKeyboardButton(text="📝 Отзывы", callback_data="reviews"),
            InlineKeyboardButton(text="ℹ️ О нас", callback_data="about_us"),
        ],
        [
            InlineKeyboardButton(text="🎁 Подари другу", callback_data="gift_friend"),
            InlineKeyboardButton(text="🤝 Партнёрка", callback_data="partner"),
        ],
        [
            InlineKeyboardButton(text="🛠 Другие сервисы", callback_data="other_services"),
            InlineKeyboardButton(text="📢 Наш канал", callback_data="our_channel"),
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