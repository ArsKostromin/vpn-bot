from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext  # Добавляем импорт для работы со state
import inspect  # Чтобы аккуратно проверять аргументы функций

router = Router()

# Импортируем реализованные колбеки
from bot.handlers.balance import balance_up_callback
from bot.handlers.vpn import start_vpn_buying
from bot.handlers.my_services import my_services_screen, profile_handler
from bot.handlers.start import help_handler, reviews, about_us, gift_friend, partners, other_services, buy_proxy


COMMAND_TO_CALLBACK = {
    "buyvpn": ("buy_vpn", start_vpn_buying),
    "myservices": ("my_services", my_services_screen),
    "account": ("account", profile_handler),
    "topup": ("balance_up", balance_up_callback),
    "help": ("help", help_handler),
    "reviews": ("reviews", reviews),
    "aboutus": ("about_us", about_us),
    "gift": ("gift_friend", gift_friend),
    "partner": ("partner", partners),
    "otherservices": ("other_services", other_services),
    "ourchannel": ("our_channel", buy_proxy),
}

@router.message(Command(*COMMAND_TO_CALLBACK.keys()))
async def handle_command_as_callback(message: Message, state: FSMContext):
    command = message.text.lstrip("/")
    if command in COMMAND_TO_CALLBACK:
        callback_data, callback_handler = COMMAND_TO_CALLBACK[command]

        fake_callback_query = CallbackQuery(
            id="fake",  # фиктивный id
            from_user=message.from_user,
            chat_instance="fake_instance",
            message=message,
            data=callback_data
        )

        # Проверяем, ожидает ли функция параметр state
        signature = inspect.signature(callback_handler)
        if "state" in signature.parameters:
            await callback_handler(fake_callback_query, state)
        else:
            await callback_handler(fake_callback_query)

