from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command

from database.crud import get_user_bookings, cancel_booking
from state.booking_state import BookingState



router = Router()




@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        '👋 Привет! Я помогу вам забронировать столик в ресторане.\n'
        'Вот что я умею:\n'
        '/book — забронировать столик\n'
        '/mybookings — ваши бронирования\n'
        '/cancel — отменить текущее бронирование'
    )


@router.message(Command('mybookings'))
async def my_bookings(message: Message):
    bookings = get_user_bookings(message.from_user.id)

    if not bookings:
        await message.answer('📭 У вас нет активных бронирований.')
        return

    text = '📋 Ваши бронирования:\n\n'
    for b in bookings:
        status = "✅ Оплачено" if b[6] else '❌ Не оплачено'
        text += (
            f'🆔 ID: {b[0]}\n'
            f'📅 {b[2]} ⏰ {b[3]} 👥 {b[4]}\n'
            f'💬 {b[5]}\n'
            f'{status}\n\n'
        )

    await message.answer(text)


@router.message(Command('cancel'))
async def cancel(message: Message):
    bookings = get_user_bookings(message.from_user.id)

    if not bookings:
        await message.answer('📭 У вас нет активных бронирований.')
        return

    text = 'Введите ID бронирования, которое хотите отменить. Ваши бронирования:\n\n'
    for b in bookings:
        text += f"🆔 {b[0]} | 📅 {b[2]} ⏰ {b[3]} 👥 {b[4]}\n"

    await message.answer(text)
    await BookingState.cancel.set()


@router.message(F.text == '/mybookings')
async def my_bookings_cmd(message: Message):
    bookings = get_user_bookings(message.from_user.id)
    if not bookings:
        await message.answer('У вас нет активных бронирований.')
    else:
        response = 'Ваши бронирования:\n'
        for b in bookings:
            response += f'📅 {b[2]} 🕒 {b[3]} 👥 {b[4]} 💬 {b[5]} {'✅ Оплачено' if b[6] else '❌ Не оплачено'}\n'
        await message.answer(response)


@router.message(F.text == '/cancel')
async def cancel_cmd(message: Message, state: FSMContext):
    cancel_booking(message.from_user.id)
    await state.clear()
    await message.answer('Ваше бронирование отменено.')



