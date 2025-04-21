# bot/keyboards/inline_main_menu.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛡 Купить VPN", callback_data="buy_vpn"),
            InlineKeyboardButton(text="🪖 Купить прокси", callback_data="buy_proxy"),
        ],
        [
            InlineKeyboardButton(text="📦 Мои услуги", callback_data="my_services"),
            InlineKeyboardButton(text="⚙️ Аккаунт", callback_data="account"),
        ],
        [
            InlineKeyboardButton(text="💳 Пополнить", callback_data="top_up"),
            InlineKeyboardButton(text="🆘 Помощь", callback_data="help"),
        ],
        [
            InlineKeyboardButton(text="✍️ Отзывы", callback_data="reviews"),
            InlineKeyboardButton(text="👥 О нас", callback_data="about_us"),
        ],
        [
            InlineKeyboardButton(text="🎁 Подари другу", callback_data="gift_friend"),
            InlineKeyboardButton(text="🤝 Партнерка", callback_data="partners"),
        ],
        [
            InlineKeyboardButton(text="🧰 Другие сервисы", callback_data="other_services"),
            InlineKeyboardButton(text="📢 Наш канал", url="https://t.me/YouFastVPN"),  # Прямая ссылка
        ]
    ]
)
