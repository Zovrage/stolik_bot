from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def time_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='18:00'), KeyboardButton(text='19:00')],
        [KeyboardButton(text='20:00'), KeyboardButton(text='21:00')]
    ], resize_keyboard=True)


def guests_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='1'), KeyboardButton(text='2'), KeyboardButton(text="3")],
        [KeyboardButton(text='4'), KeyboardButton(text='5'), KeyboardButton(text="6+")]
    ], resize_keyboard=True)


def preferences_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='У окна')],
        [KeyboardButton(text='В зале')],
        [KeyboardButton(text='Не важно')]
    ], resize_keyboard=True)