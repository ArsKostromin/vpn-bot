#handlers/balance.py тут пополнение баланса
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice
from bot.keyboards.balance_menu import get_star_topup_menu, get_crypto_currency_keyboard, get_balance_menu, start_balance, get_balance_menu_roboc, end_upbalance
from bot.services.upbalance import create_payment_link, create_crypto_payment
import traceback

router = Router()



@router.callback_query(F.data == "balance_up")
async def balance_up_callback(call: CallbackQuery):
    await call.bot.send_photo(
        chat_id=call.message.chat.id,
        photo="https://play-lh.googleusercontent.com/BFkf2bgtxsCvsTnR2yw8yuWD3mgpThoyiRoBhoazTqFFMNOmdxGAAqS7vMATyNwelQ",
        caption="🔥 Выберите крипту или Робокассу",
        reply_markup=start_balance,
    )


# Показываем меню пополнения
@router.callback_query(F.data == "robokassa")
async def balance_menu_callback(call: CallbackQuery):
    await call.message.answer(
        "Выберите сумму пополнения:",
        reply_markup=get_balance_menu_roboc()
    )
    await call.answer()

# Обрабатываем выбор суммы
@router.callback_query(F.data.startswith("topup_"))
async def process_topup(callback: CallbackQuery):
    amount_str = callback.data.split("_")[1]
    amount = int(amount_str)

    try:
        payment_link = await create_payment_link(telegram_id=callback.from_user.id, amount=amount)
        await callback.message.answer(f"Вот ваша ссылка для оплаты на {amount} ₽:\n{payment_link}", reply_markup=end_upbalance)
        await callback.answer()
    except Exception as e:
        await callback.message.answer("Ошибка при создании платежа. Попробуйте позже.", reply_markup=end_upbalance)
        await callback.answer()

# Обработка кнопки "Назад"
@router.callback_query(F.data == "back_to_menu")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.answer("Вы вернулись в главное меню.")
    await callback.answer()



#crypt

# Когда пользователь нажимает "Пополнить баланс"
@router.callback_query(F.data == "cryptobot")
async def balance_up_start(call: CallbackQuery):
    await call.message.answer(
        "💵 Выберите сумму для пополнения:",
        reply_markup=get_balance_menu()
    )


@router.callback_query(F.data.startswith("balance_amount_"))
async def choose_crypto(call: CallbackQuery):
    amount = int(call.data.split("_")[-1])
    await call.message.answer(
        "💱 Выберите криптовалюту для оплаты:",
        reply_markup=get_crypto_currency_keyboard(amount)
    )


# Когда пользователь выбрал сумму
@router.callback_query(F.data.startswith("crypto_"))
async def create_payment(call: CallbackQuery):
    try:
        _, asset, amount_str = call.data.split("_")
        amount = int(amount_str)
    except (ValueError, IndexError):
        await call.message.answer("❌ Неверные данные для оплаты. Попробуйте снова.")
        return

    telegram_id = call.from_user.id

    try:
        payment_url = await create_crypto_payment(telegram_id, amount, asset)
        await call.message.answer(
            f"🧾 Оплата на сумму {amount} ₽ через {asset} создана!\n\n"
            f"👉 Перейдите по ссылке: {payment_url}",
            reply_markup=end_upbalance
        )
    except Exception as e:
        import logging, traceback
        logging.error(f"Ошибка при создании платежа для {telegram_id}: {e}")
        logging.error(traceback.format_exc())
        await call.message.answer("❌ Ошибка при создании платежа. Попробуйте позже.")


#telegram stars
STAR_PRICE_RUB = 1.79

@router.callback_query(F.data == "tgstars")
async def open_star_menu(callback: CallbackQuery):
    await callback.message.answer("Выберите сумму пополнения через звёзды:", reply_markup=get_star_topup_menu())
    await callback.answer()



@router.callback_query(F.data.startswith("tgstars_"))
async def process_star_topup(callback: CallbackQuery):
    amount_rub = int(callback.data.split("_")[1])
    stars = int(amount_rub / STAR_PRICE_RUB)

    prices = [
        LabeledPrice(label=f"{stars} звёзд", amount=stars * 100)  # в копейках
    ]

    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Пополнение баланса",
        description=f"Вы пополняете баланс на {amount_rub}₽",
        payload=f"user_{callback.from_user.id}_rub_{amount_rub}",
        provider_token="robokassa:VPN.RU:wc4vj9gdLQXs2nhrL1n2",  # ⚠️ замените!
        currency="RUB",
        prices=prices,
        start_parameter="stars-payment"
    )

    await callback.answer()
    
    
@router.message(F.successful_payment)
async def handle_star_payment(message: Message):
    total_amount = message.successful_payment.total_amount
    currency = message.successful_payment.currency

    stars = total_amount / 100
    telegram_id = message.from_user.id

    payment = await register_star_payment(user_id=telegram_id, stars=stars)

    await message.answer(f"✅ Успешно! На ваш баланс зачислено {payment['amount']}₽ за {int(stars)} ⭐.")
