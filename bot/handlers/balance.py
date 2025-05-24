from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext

from bot.keyboards.balance_menu import (
    get_crypto_currency_keyboard,
    get_balance_menu,
    start_balance,
    get_balance_menu_roboc,
    end_upbalance,
)
from bot.services.upbalance import (
    create_payment_link,
    create_crypto_payment,
    register_star_payment,
    STAR_PRICE_RUB,
)
import logging
import traceback
from bot.states.upbalance import TopUpStates
from aiogram import types
from decimal import Decimal
from aiogram.exceptions import TelegramBadRequest
import asyncio
from bot.services.cryptomus import make_request, check_invoice_paid
import uuid


router = Router()


# 📲 Главное меню пополнения
@router.callback_query(F.data == "balance_up")
async def balance_up_callback(call: CallbackQuery):
    await call.bot.send_photo(
        chat_id=call.message.chat.id,
        photo="https://play-lh.googleusercontent.com/BFkf2bgtxsCvsTnR2yw8yuWD3mgpThoyiRoBhoazTqFFMNOmdxGAAqS7vMATyNwelQ",
        caption="🔥 Выберите способ оплаты",
        reply_markup=start_balance,
    )


# 💳 Меню Робокассы
@router.callback_query(F.data == "robokassa")
async def balance_menu_callback(call: CallbackQuery):
    await call.message.answer(
        "Выберите сумму пополнения:",
        reply_markup=get_balance_menu_roboc()
    )
    await call.answer()


# 🧾 Обработка выбора суммы для Робокассы
@router.callback_query(F.data.startswith("topup_"))
async def process_topup(callback: CallbackQuery, state: FSMContext):
    amount_str = callback.data.split("_")[1]
    
    if amount_str == "custom":
        # Перенаправляем на FSM
        await callback.message.answer("Введите сумму пополнения в рублях (например, 250):")
        await state.set_state(TopUpStates.waiting_for_custom_amount)
        await callback.answer()
        return

    try:
        amount = int(amount_str)
        payment_link = await create_payment_link(telegram_id=callback.from_user.id, amount=amount)
        await callback.message.answer(
            f"Вот ваша ссылка для оплаты на {amount} ₽:\n{payment_link}",
            reply_markup=end_upbalance
        )
        await callback.answer()
    except Exception:
        await callback.message.answer("Ошибка при создании платежа. Попробуйте позже.", reply_markup=end_upbalance)
        await callback.answer()



# 🔙 Назад в меню
@router.callback_query(F.data == "back_to_menu")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.answer("Вы вернулись в главное меню.")
    await callback.answer()
    

# обработка кнопки "💰 Ввести свою сумму"
@router.callback_query(F.data == "topup_custom")
async def process_custom_amount_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите сумму пополнения в рублях (например, 250):")
    await state.set_state(TopUpStates.waiting_for_custom_amount)
    await callback.answer()

# обработка пользовательского ввода суммы
@router.message(TopUpStates.waiting_for_custom_amount)
async def process_custom_amount_input(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount < 5:
            await message.answer("Минимальная сумма пополнения — 5 $. Попробуйте снова.")
            return

        payment_link = await create_payment_link(telegram_id=message.from_user.id, amount=amount)
        await message.answer(
            f"Вот ваша ссылка для оплаты на {amount} :\n{payment_link}",
            reply_markup=end_upbalance
        )
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите число. Пример: 150")
    except Exception as e:
        logging.error(traceback.format_exc())
        await message.answer("Ошибка при создании платежа. Попробуйте позже.")
        await state.clear()



# ₿ Крипта: выбор суммы
@router.callback_query(F.data == "cryptobot")
async def balance_up_start(call: CallbackQuery):
    logging.debug(f"callback_query: cryptobot | from_user={call.from_user.id}")
    try:
        await call.message.edit_text(
            "💸 Выбери сумму пополнения:",
            reply_markup=get_balance_menu()
        )
    except TelegramBadRequest as e:
        logging.warning(f"TelegramBadRequest: {e}")
        if "there is no text in the message to edit" in str(e):
            await call.message.answer(
                "💸 Выбери сумму пополнения:",
                reply_markup=get_balance_menu()
            )
        else:
            raise


@router.callback_query(F.data.startswith("balance_amount_"))
async def select_crypto_currency(call: CallbackQuery):
    logging.debug(f"callback_query: {call.data} | from_user={call.from_user.id}")
    amount = int(call.data.split("_")[-1])
    await call.message.edit_text(
        f"Выбери криптовалюту для пополнения на {amount}$:",
        reply_markup=get_crypto_currency_keyboard(amount)
    )


@router.callback_query(F.data.startswith("crypto_"))
async def start_crypto_payment(call: CallbackQuery):
    logging.debug(f"callback_query: {call.data} | from_user={call.from_user.id}")
    _, currency, amount = call.data.split("_")
    amount = int(amount)
    order_id = f"user_{call.from_user.id}_{amount}_{uuid.uuid4().hex}"

    invoice_data = {
        "amount": str(amount),
        "currency": currency.upper(),
        "order_id": order_id,
        "url_callback": "https://server2.anonixvpn.space/payments/api/crypto/webhook/",
        "url_return": "https://t.me/fastvpnVPNs_bot",
        "is_payment_multiple": False,
        "lifetime": 900,
    }

    networks_required = {
        "USDT": "TRON",
        "USDC": "POLYGON",
        "TON": "TON",
        "ETH": "ERC20",
        "BNB": "BEP20",
        "LTC": "LTC",
        "BTC": "BTC"
    }

    if currency.upper() in networks_required:
        invoice_data["network"] = networks_required[currency.upper()]

    try:
        logging.info(f"Creating invoice: {invoice_data}")
        response = await make_request(
            url="https://api.cryptomus.com/v1/payment",
            invoice_data=invoice_data
        )
        logging.info(f"Cryptomus response: {response}")
        invoice_url = response["result"]["url"]
        invoice_uuid = response["result"]["uuid"]

        asyncio.create_task(check_invoice_paid(invoice_uuid, call.message))

        await call.message.edit_text(
            f"🔗 Вот твоя ссылка для оплаты:\n\n{invoice_url}",
            reply_markup=end_upbalance
        )
    except Exception as e:
        logging.error(f"❌ Ошибка при создании платежа: {e}", exc_info=True)
        await call.message.answer(f"❌ Ошибка при создании платежа: {e}")