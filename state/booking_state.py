from aiogram.fsm.state import StatesGroup, State

class BookingState(StatesGroup):
    date = State()
    time = State()
    guests = State()
    preferences = State()
    cancel = State()