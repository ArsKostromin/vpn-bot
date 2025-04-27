from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

my_services_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="продлить", callback_data="my_vpn"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="start_from_button"),
        ]
    ]
)


not_subscription = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Купить", callback_data="buy_vpn"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="start_from_button"),
        ]
    ]
)

# buy_proxy_keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="📲 Мобильные", callback_data="buy_mobile"),
#             InlineKeyboardButton(text="🏠 Резидентские", callback_data="buy_residential"),
#         ],
#         [
#             InlineKeyboardButton(text="🔁 Резидентские с ротацией", callback_data="buy_rotating"),
#         ],
#         [
#             InlineKeyboardButton(text="⬅️ Назад", callback_data="back_proxy"),
#         ],
#     ]
# )