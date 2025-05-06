#handlers/balance.py тут пополнение баланса
from aiogram import Router, F
from bot.keyboards.balance_menu import get_star_topup_menu, get_crypto_currency_keyboard, get_balance_menu, start_balance, get_balance_menu_roboc, end_upbalance, get_star_topup_menu
from bot.services.upbalance import create_payment_link, create_crypto_payment, register_star_payment, STAR_PRICE_RUB
import traceback
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery

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


#telegram stars handlers/balance.py

@router.callback_query(F.data == "tgstars")
async def open_star_menu(callback: CallbackQuery):
    await callback.message.answer(
        "💫 Выберите сумму пополнения через звёзды:",
        reply_markup=get_star_topup_menu()
    )
    await callback.answer()


from aiogram.types import LabeledPrice, Message, InlineKeyboardMarkup, InlineKeyboardButton

@router.callback_query(F.data.startswith("tgstars_"))
async def process_star_topup(callback: CallbackQuery, state: FSMContext):
    amount_rub = int(callback.data.split("_")[1])
    stars_needed = round(amount_rub / STAR_PRICE_RUB)

    await callback.message.answer(
        f"🎁 Чтобы пополнить баланс на <b>{amount_rub}₽</b>, "
        f"подарите <b>{stars_needed} звёзд</b> этому боту прямо в этом чате.\n\n"
        f"Нажмите на кнопку ниже, чтобы подарить ⭐️:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Подарить ⭐️", pay=True)],
                [InlineKeyboardButton("🔙 Назад", callback_data="tgstars")]
            ]
        )
    )
    await callback.answer()

    
    
@router.message(F.gifted_stars)
async def handle_gifted_stars(message: Message):
    if not message.gifted_stars:
        return

    stars = message.gifted_stars.gift.count
    user_id = message.from_user.id

    try:
        payment = await register_star_payment(user_id=user_id, stars=stars)
        amount = payment.get("amount", 0)

        await message.answer(
            f"✅ Спасибо за {stars} ⭐!\n"
            f"💸 На ваш баланс зачислено <b>{amount}₽</b>.",
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer("❌ Произошла ошибка при зачислении звёзд.")