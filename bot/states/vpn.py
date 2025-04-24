# states/vpn.py

from aiogram.fsm.state import State, StatesGroup

class BuyVPN(StatesGroup):
    vpn_type = State()
    duration = State()
