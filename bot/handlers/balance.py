from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext

from bot.keyboards.balance_menu import (
    get_star_topup_menu,
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
from bot.services.cryptomus import create_cryptomus_invoice
import logging
import traceback
from bot.states.upbalance import TopUpStates
from aiogram import types
from decimal import Decimal
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
    try:
        await call.message.edit_text(
            "💸 Выбери сумму пополнения:",
            reply_markup=get_balance_menu()
        )
    except TelegramBadRequest as e:
        if "there is no text in the message to edit" in str(e):
            # Используем send_message как fallback
            await call.message.answer(
                "💸 Выбери сумму пополнения:",
                reply_markup=get_balance_menu()
            )
            # Или: сначала удаляем старое сообщение
            # await call.message.delete()
            # await call.message.answer("💸 Выбери сумму пополнения:", reply_markup=get_balance_menu())
        else:
            raise


@router.callback_query(F.data.startswith("balance_amount_"))
async def select_crypto_currency(call: CallbackQuery):
    amount = int(call.data.split("_")[-1])
    await call.message.edit_text(
        f"Выбери криптовалюту для пополнения на {amount}$:",
        reply_markup=get_crypto_currency_keyboard(amount)
    )


@router.callback_query(F.data.startswith("crypto_"))
async def start_crypto_payment(call: CallbackQuery):
    _, currency, amount = call.data.split("_")
    amount = int(amount)

    url = await create_cryptomus_invoice(amount, currency, call.from_user.id)

    await call.message.edit_text(
        f"🔗 Вот твоя ссылка для оплаты:\n\n{url}",
        reply_markup=end_upbalance
    )
