# states/vpn.py
from aiogram.fsm.state import State, StatesGroup

class BuyVPN(StatesGroup):
    vpn_type = State()
    duration = State()
    confirmation = State()  # добавлено состояние подтверждения
    waiting_for_topup = State()  # новое состояние: ожидание пополнения
