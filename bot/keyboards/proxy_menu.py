from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

proxy_service_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🧦 Купить", callback_data="buy_proxy2"),
            InlineKeyboardButton(text="📎 Мои прокси", callback_data="my_proxies"),
        ],
        [
            InlineKeyboardButton(text="🔓 IP Чекер", callback_data="ip_checker"),
            InlineKeyboardButton(text="❓ О сервисе", callback_data="about_service"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main"),
        ]
    ]
)

buy_proxy_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📲 Мобильные", callback_data="buy_mobile"),
            InlineKeyboardButton(text="🏠 Резидентские", callback_data="buy_residential"),
        ],
        [
            InlineKeyboardButton(text="🔁 Резидентские с ротацией", callback_data="buy_rotating"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_proxy"),
        ],
    ]
)