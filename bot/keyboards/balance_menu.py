from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_balance_menu_roboc():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=" 7 $", callback_data="topup_7"),
            InlineKeyboardButton(text="15 $", callback_data="topup_15"),
            InlineKeyboardButton(text="27 $", callback_data="topup_27"),
            InlineKeyboardButton(text="48 $", callback_data="topup_48"),

        ],
        [
            InlineKeyboardButton(text="💰 Ввести сумму", callback_data="topup_custom")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="balance_up")
        ],
    ])
    return keyboard

start_balance = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💳 Карты и QR-код", callback_data="robokassa"),
        ],
        [
            InlineKeyboardButton(text="Крипта", callback_data="cryptobot"),
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
            [InlineKeyboardButton(text="7 $", callback_data="balance_amount_7"),
            InlineKeyboardButton(text="15 $", callback_data="balance_amount_15"),
            InlineKeyboardButton(text="27 $", callback_data="balance_amount_27"),
            InlineKeyboardButton(text="48 $", callback_data="balance_amount_48")],
            
            [InlineKeyboardButton(text="💰 Ввести сумму", callback_data="cryptotopup_custom")],
            
            [InlineKeyboardButton(text="Назад", callback_data="balance_up")],
        ]
    )


end_upbalance = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Посмотреть баланс", callback_data="account"),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="start_from_button")
        ],
    ]
)

def get_crypto_currency_keyboard(amount: int) -> InlineKeyboardMarkup:
    supported_currencies = [
        "TON", "USDT", "USDC",
        "BTC", "BNB", "LTC"
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

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_qr_code_keyboard(address: str, qr_code: str, amount: str, currency: str) -> InlineKeyboardMarkup:
    """
    Клавиатура для отображения QR-кода с кнопками копирования
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Скопировать адрес", 
                    callback_data="copy_address"
                ),
                InlineKeyboardButton(
                    text="📱 Скопировать QR", 
                    callback_data="copy_qr"
                )
            ],
            [
                InlineKeyboardButton(text="🔄 Проверить оплату", callback_data="check_payment"),
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data="balance_up")
            ],
        ]
    )
