from aiogram.fsm.state import State, StatesGroup

class CouponState(StatesGroup):
    waiting_for_code = State()
