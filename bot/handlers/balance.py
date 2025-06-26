from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile,
)
from aiogram.fsm.context import FSMContext
from bot.keyboards.balance_menu import (
    get_crypto_currency_keyboard,
    get_balance_menu,
    start_balance,
    get_balance_menu_roboc,
    end_upbalance,
    get_qr_code_keyboard,
)
from bot.services.upbalance import (
    create_payment_link,
    create_crypto_payment,
    register_star_payment,
    STAR_PRICE_RUB,
)
import logging
import traceback
from bot.states.upbalance import TopUpStates, CryptoTopUpStates
from aiogram.exceptions import TelegramBadRequest
import asyncio
from bot.services.cryptomus import make_request, check_invoice_paid, extract_wallet_info
import uuid


router = Router()


# 📲 Главное меню пополнения
@router.callback_query(F.data == "balance_up")
async def balance_up_callback(call: CallbackQuery):
    await call.bot.send_photo(
        chat_id=call.message.chat.id,
        photo = FSInputFile("bot/media/anonix.jpg"),
        caption="🔥 Выберите способ оплаты",
        reply_markup=start_balance,
    )


# 💳 Меню Робокассы
@router.callback_query(F.data == "robokassa")
async def balance_menu_callback(call: CallbackQuery):
    await call.message.answer(
        "💸 Выберите сумму пополнения:",
        reply_markup=get_balance_menu_roboc()
    )
    await call.answer()


# 🧾 Обработка выбора суммы для Робокассы
@router.callback_query(F.data.startswith("topup_"))
async def process_topup(callback: CallbackQuery, state: FSMContext):
    amount_str = callback.data.split("_")[1]

    if amount_str == "custom":
        await callback.message.answer("Введите сумму пополнения в долларах (например, 250):")
        await state.set_state(TopUpStates.waiting_for_custom_amount)
        await callback.answer()
        return

    try:
        amount = int(amount_str)
        payment_link = await create_payment_link(telegram_id=callback.from_user.id, amount=amount)
        await callback.message.answer(
            f"Вот ваша ссылка для оплаты на {amount} $:\n{payment_link}\nсредства поступят на счет в течение 3-5 мин после оплаты",
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


# обработка кнопки "💰 Ввести свою сумму" (Робокасса)
@router.callback_query(F.data == "topup_custom")
async def process_custom_amount_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите сумму пополнения в долларах (например, 250):")
    await state.set_state(TopUpStates.waiting_for_custom_amount)
    await callback.answer()


# обработка пользовательского ввода суммы (Робокасса)
@router.message(TopUpStates.waiting_for_custom_amount)
async def process_custom_amount_input(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount < 1:
            await message.answer("Минимальная сумма пополнения — 1 $. Попробуйте снова.")
            return

        payment_link = await create_payment_link(telegram_id=message.from_user.id, amount=amount)
        await message.answer(
            f"Вот ваша ссылка для оплаты на {amount} $:\n{payment_link} \nсредства поступят на счет в течение 3-5 мин после оплаты",
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
            "💸 Выберите сумму пополнения:",
            reply_markup=get_balance_menu()
        )
    except TelegramBadRequest as e:
        logging.warning(f"TelegramBadRequest: {e}")
        if "there is no text in the message to edit" in str(e):
            await call.message.answer(
                "💸 Выберите сумму пополнения:",
                reply_markup=get_balance_menu()
            )
        else:
            raise


# обработка кнопок 1/100/500$
@router.callback_query(F.data.startswith("balance_amount_"))
async def select_crypto_currency(call: CallbackQuery):
    logging.debug(f"callback_query: {call.data} | from_user={call.from_user.id}")
    amount = int(call.data.split("_")[-1])
    await call.message.edit_text(
        f"Выберите криптовалюту для пополнения на {amount}$:",
        reply_markup=get_crypto_currency_keyboard(amount)
    )


# обработка кнопки "💰 Ввести свою сумму" (Крипта)
@router.callback_query(F.data == "cryptotopup_custom")
async def process_custom_amount_request_crypto(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите сумму пополнения в долларах (например, 250):")
    await state.set_state(CryptoTopUpStates.waiting_for_custom_amount)
    await callback.answer()


# обработка пользовательского ввода суммы (Крипта)
@router.message(CryptoTopUpStates.waiting_for_custom_amount)
async def process_custom_crypto_amount_input(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount < 1:
            await message.answer("Минимальная сумма пополнения — 1 $. Попробуйте снова.")
            return

        await message.answer(
            f"Выберите криптовалюту для пополнения на {amount} $:",
            reply_markup=get_crypto_currency_keyboard(amount)
        )
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите число. Пример: 150")
    except Exception as e:
        logging.error(traceback.format_exc())
        await message.answer("Ошибка. Попробуйте позже.")
        await state.clear()


# запуск криптоплатежа
@router.callback_query(F.data.startswith("crypto_"))
async def start_crypto_payment(call: CallbackQuery, state: FSMContext):
    logging.debug(f"callback_query: {call.data} | from_user={call.from_user.id}")
    _, currency, amount = call.data.split("_")
    amount = int(amount)
    order_id = f"user_{call.from_user.id}_{amount}_{uuid.uuid4().hex}"

    invoice_data = {
        "amount": str(amount),                    # Сумма в долларах
        "currency": "USD",                        # Пользователь платит 50 USD
        "to_currency": currency.upper(),          # А платёж произойдёт, например, в BTC
        "order_id": order_id,
        "url_callback": "https://server2.anonixvpn.space/payments/api/crypto/webhook/",
        "url_return": "https://t.me/Anonixvpn_vpnBot",
        "is_payment_multiple": False,
        "lifetime": 900,
        "is_test": True,
    }


    networks_required = {
        "USDT": "TRON",
        "USDC": "ETH",
        "ETH": "ARBITRUM",
        "BNB": "BSC",
        "LTC": "LTC",
        "BTC": "BTC",
        "TON": "TON"
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
        
        # Извлекаем информацию о кошельке
        wallet_info = extract_wallet_info(response)
        
        if wallet_info.get("address") and wallet_info.get("qr_code"):
            # Сохраняем информацию о кошельке в состоянии
            await state.update_data(
                wallet_address=wallet_info['address'],
                wallet_qr_code=wallet_info['qr_code'],
                payment_amount=wallet_info['amount'],
                payment_currency=wallet_info['currency'],
                payment_uuid=wallet_info.get('uuid'),
                original_amount=amount,
                original_currency=currency
            )
            await state.set_state(CryptoTopUpStates.waiting_for_payment)
            
            # Проверяем, является ли QR-код URL-ом
            qr_code = wallet_info['qr_code']
            is_qr_url = qr_code.startswith('http')
            
            if is_qr_url:
                # Отправляем QR-код как изображение
                try:
                    await call.message.answer_photo(
                        photo=qr_code,
                        caption=(
                            f"💳 Оплата {amount}$ в {currency.upper()}\n\n"
                            f"🏦 Адрес кошелька:\n"
                            f"`{wallet_info['address']}`\n\n"
                            f"💰 Сумма к оплате: {wallet_info['amount']} {wallet_info['currency']}\n\n"
                            f"⏰ Время на оплату: 15 минут\n"
                            f"✅ После оплаты баланс пополнится автоматически"
                        ),
                        parse_mode="Markdown"
                    )
                    
                    # Создаем специальную клавиатуру для QR-кода
                    qr_keyboard = get_qr_code_keyboard(
                        address=wallet_info['address'],
                        qr_code=wallet_info['qr_code'],
                        amount=wallet_info['amount'],
                        currency=wallet_info['currency']
                    )
                    
                    await call.message.answer(
                        "📱 Используйте кнопки ниже для копирования:",
                        reply_markup=qr_keyboard
                    )
                except Exception as e:
                    logging.error(f"Ошибка при отправке QR-кода как изображения: {e}")
                    # Fallback на текстовый формат
                    qr_message = (
                        f"💳 Оплата {amount}$ в {currency.upper()}\n\n"
                        f"📱 QR-код для оплаты:\n"
                        f"`{qr_code}`\n\n"
                        f"🏦 Адрес кошелька:\n"
                        f"`{wallet_info['address']}`\n\n"
                        f"💰 Сумма к оплате: {wallet_info['amount']} {wallet_info['currency']}\n\n"
                        f"⏰ Время на оплату: 15 минут\n"
                        f"✅ После оплаты баланс пополнится автоматически"
                    )
                    
                    # Создаем специальную клавиатуру для QR-кода
                    qr_keyboard = get_qr_code_keyboard(
                        address=wallet_info['address'],
                        qr_code=wallet_info['qr_code'],
                        amount=wallet_info['amount'],
                        currency=wallet_info['currency']
                    )
                    
                    await call.message.edit_text(
                        qr_message,
                        reply_markup=qr_keyboard,
                        parse_mode="Markdown"
                    )
            else:
                # Отправляем QR-код как текст
                qr_message = (
                    f"💳 Оплата {amount}$ в {currency.upper()}\n\n"
                    f"📱 QR-код для оплаты:\n"
                    f"`{qr_code}`\n\n"
                    f"🏦 Адрес кошелька:\n"
                    f"`{wallet_info['address']}`\n\n"
                    f"💰 Сумма к оплате: {wallet_info['amount']} {wallet_info['currency']}\n\n"
                    f"⏰ Время на оплату: 15 минут\n"
                    f"✅ После оплаты баланс пополнится автоматически"
                )
                
                # Создаем специальную клавиатуру для QR-кода
                qr_keyboard = get_qr_code_keyboard(
                    address=wallet_info['address'],
                    qr_code=wallet_info['qr_code'],
                    amount=wallet_info['amount'],
                    currency=wallet_info['currency']
                )
                
                await call.message.edit_text(
                    qr_message,
                    reply_markup=qr_keyboard,
                    parse_mode="Markdown"
                )
            
            # Запускаем проверку оплаты
            if wallet_info.get("uuid"):
                asyncio.create_task(check_invoice_paid(wallet_info["uuid"], call.message, state))
        else:
            # Fallback на старый способ с ссылкой
            invoice_url = response["result"]["url"]
            invoice_uuid = response["result"]["uuid"]

            asyncio.create_task(check_invoice_paid(invoice_uuid, call.message, state))

            await call.message.edit_text(
                f"🔗 Вот твоя ссылка для оплаты:\n\n{invoice_url}",
                reply_markup=end_upbalance
            )
    except Exception as e:
        logging.error(f"❌ Ошибка при создании платежа: {e}", exc_info=True)
        await call.message.answer(f"❌ Ошибка при создании платежа: {e}")


# Обработчик копирования адреса кошелька
@router.callback_query(F.data == "copy_address")
async def copy_wallet_address(call: CallbackQuery, state: FSMContext):
    try:
        # Получаем данные из состояния
        data = await state.get_data()
        wallet_address = data.get('wallet_address')
        
        if wallet_address:
            # В реальном приложении здесь можно использовать clipboard API
            # Пока просто показываем адрес в уведомлении
            await call.answer(f"Адрес: {wallet_address}", show_alert=True)
        else:
            await call.answer("Адрес не найден", show_alert=True)
    except Exception as e:
        await call.answer("Ошибка при копировании", show_alert=True)


# Обработчик копирования QR-кода
@router.callback_query(F.data == "copy_qr")
async def copy_qr_code(call: CallbackQuery, state: FSMContext):
    try:
        # Получаем данные из состояния
        data = await state.get_data()
        wallet_qr_code = data.get('wallet_qr_code')
        
        if wallet_qr_code:
            # В реальном приложении здесь можно использовать clipboard API
            # Пока просто показываем QR-код в уведомлении
            await call.answer(f"QR-код: {wallet_qr_code}", show_alert=True)
        else:
            await call.answer("QR-код не найден", show_alert=True)
    except Exception as e:
        await call.answer("Ошибка при копировании", show_alert=True)


# Обработчик проверки оплаты
@router.callback_query(F.data == "check_payment")
async def check_payment_status(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        payment_uuid = data.get('payment_uuid')
        
        if payment_uuid:
            await call.answer("Проверяем статус оплаты...", show_alert=True)
            
            # Проверяем статус через API
            try:
                invoice_data = await make_request(
                    url="https://api.cryptomus.com/v1/payment/info",
                    invoice_data={"uuid": payment_uuid},
                )
                
                status = invoice_data["result"].get("payment_status")
                
                if status in ("paid", "paid_over"):
                    await call.message.answer("✅ Оплата прошла успешно! Баланс пополнен.")
                    await state.clear()
                elif status == "pending":
                    await call.message.answer("⏳ Платёж в обработке. Попробуйте проверить позже.")
                else:
                    await call.message.answer(f"❌ Статус платежа: {status}\nПлатёж ещё не поступил.")
                    
            except Exception as e:
                logging.error(f"Ошибка при проверке статуса: {e}")
                await call.message.answer("❌ Ошибка при проверке статуса. Попробуйте позже.")
        else:
            await call.answer("Информация о платеже не найдена", show_alert=True)
    except Exception as e:
        await call.answer("Ошибка при проверке", show_alert=True)
