from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_balance_menu_roboc():
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



def get_balance_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1 руб", callback_data="balance_amount_1")],
            [InlineKeyboardButton(text="100 руб", callback_data="balance_amount_100")],
            [InlineKeyboardButton(text="500 руб", callback_data="balance_amount_500")],
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

def get_crypto_currency_keyboard(amount: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="TON", callback_data=f"crypto_TON_{amount}")],
        [InlineKeyboardButton(text="USDT", callback_data=f"crypto_USDT_{amount}")],
        [InlineKeyboardButton(text="BTC", callback_data=f"crypto_BTC_{amount}")],
        [InlineKeyboardButton(text="ETH", callback_data=f"crypto_ETH_{amount}")],
        [InlineKeyboardButton(text="LTC", callback_data=f"crypto_LTC_{amount}")],
        [InlineKeyboardButton(text="BNB", callback_data=f"crypto_BNB_{amount}")],
    ])