from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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