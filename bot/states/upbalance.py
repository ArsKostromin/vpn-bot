from aiogram.fsm.state import State, StatesGroup

class TopUpStates(StatesGroup):
    waiting_for_custom_amount = State()

class CryptoTopUpStates(StatesGroup):
    waiting_for_custom_amount = State()
    waiting_for_payment = State()  # Состояние ожидания оплаты
