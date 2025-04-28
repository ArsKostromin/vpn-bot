from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Главное меню")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Меню",
    is_persistent=True
)
