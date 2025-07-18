# states/vpn.py
from aiogram.fsm.state import State, StatesGroup

class BuyVPN(StatesGroup):
    vpn_type = State()
    duration = State()
    confirmation = State()  # добавлено состояние подтверждения
    # --- Новые состояния для возврата к оплате ---
    waiting_for_payment = State()
    last_vpn_type = State()
    last_duration = State()
    last_country = State()
    last_country_display = State()