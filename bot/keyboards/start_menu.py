from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_instruction_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="📥 Инструкция", 
            url="https://yourwebsite.com/instruction"
        ),
    ],
    [
        InlineKeyboardButton(
            text="🤖 Перейти в бота", 
            callback_data="start_from_button"
        ),
        InlineKeyboardButton(
            text="❓ Задать вопрос", 
            callback_data="not_ready"
        ),
    ],
    # [
    #     InlineKeyboardButton(
    #         text="🔗 Показать VPN ключ", 
    #         callback_data="show_vless_key"
    #     ),
    # ]
])
