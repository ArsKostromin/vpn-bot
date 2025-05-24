from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_balance_menu_roboc():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=" 1 $", callback_data="topup_1"),
            InlineKeyboardButton(text="100 $", callback_data="topup_100"),
            InlineKeyboardButton(text="500 $", callback_data="topup_500"),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="start_from_button")
        ],
        [
            InlineKeyboardButton(text="💰 Ввести свою сумму", callback_data="topup_custom")
        ],

    ])
    return keyboard

start_balance = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💳 карты и Qкод", callback_data="robokassa"),
        ],
        [
            InlineKeyboardButton(text="cryptobot", callback_data="cryptobot"),
        ],
        [
            InlineKeyboardButton(text="Telegram stars", url="https://t.me/Anonixvpnpaybot"),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="start_from_button")
        ],
    ]
)


def get_balance_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1 $", callback_data="balance_amount_1")],
            [InlineKeyboardButton(text="100 $", callback_data="balance_amount_100")],
            [InlineKeyboardButton(text="500 $", callback_data="balance_amount_500")],
            [InlineKeyboardButton(text="💰 Ввести свою сумму", callback_data="topup_custom")],
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

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_crypto_currency_keyboard(amount: int) -> InlineKeyboardMarkup:
    supported_currencies = [
        "TON", "USDT", "USDC",
        "BTC", "ETH", "BNB", "LTC"
    ]

    keyboard = []
    row = []
    for i, currency in enumerate(supported_currencies, start=1):
        row.append(InlineKeyboardButton(text=currency, callback_data=f"crypto_{currency}_{amount}"))
        if i % 2 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # 💰 Добавляем кнопку "Своя сумма" отдельной строкой
    keyboard.append([
        InlineKeyboardButton(text="💰 Ввести свою сумму", callback_data="topup_custom_crypto")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
