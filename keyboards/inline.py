from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def payment_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Оплатить депозит', callback_data='pay_deposit')]
    ])