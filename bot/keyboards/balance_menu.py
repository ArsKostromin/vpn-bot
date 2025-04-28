from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_balance_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=" 1 ₽", callback_data="topup_1"),
            InlineKeyboardButton(text="100 ₽", callback_data="topup_100"),
            InlineKeyboardButton(text="500 ₽", callback_data="topup_500"),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="start_from_button")
        ]
    ])
    return keyboard


start_balance = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💳 робокасса", callback_data="robokassa"),
        ],
        [
            InlineKeyboardButton(text="cryptobot", callback_data="cryptobot"),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="start_from_button")
        ],
    ]
)



def get_balance_menu_roboc():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1 Ton", callback_data="balance_amount_1")],
            [InlineKeyboardButton(text="100 Ton", callback_data="balance_amount_100")],
            [InlineKeyboardButton(text="500 Ton", callback_data="balance_amount_500")],
            [InlineKeyboardButton(text="Назад", callback_data="start_from_button")],
        ]
    )


end_upbalance = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="посмотреть баланс", callback_data="account"),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="start_from_button")
        ],
    ]
)