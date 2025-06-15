from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from datetime import datetime

from state.booking_state import BookingState
from database.crud import add_booking
from keyboards.reply import time_keyboard, guests_keyboard, preferences_keyboard
from keyboards.inline import payment_keyboard

router = Router()


@router.message(F.text == '/book')
async def start_booking(message: Message, state: FSMContext):
    await message.answer('Введите дату бронирования (в формате ДД-ММ-ГГГГ):')
    await state.set_state(BookingState.date)


@router.message(BookingState.date)
async def get_date(message: Message, state: FSMContext):
    try:
        date_obj = datetime.strptime(message.text, "%Y-%m-%d").date()
        if date_obj < datetime.today().date():
            raise ValueError('Дата в прошлом')
    except ValueError:
        await message.answer('❌ Неверный формат даты. Введите в формате ДД-ММ-ГГГГ и не в прошлом.')
        return

    await state.update_data(date=message.text)
    await message.answer('Выберите время:', reply_markup=time_keyboard())
    await state.set_state(BookingState.time)


@router.message(BookingState.time)
async def get_time(message: Message, state: FSMContext):
    allowed_times = {'18:00', '19:00', '20:00', '21:00'}
    if message.text not in allowed_times:
        await message.answer('❌ Пожалуйста, выберите время из предложенных вариантов.')
        return

    await state.update_data(time=message.text)
    await message.answer('Сколько гостей?', reply_markup=guests_keyboard())
    await state.set_state(BookingState.guests)


@router.message(BookingState.guests)
async def get_guests(message: Message, state: FSMContext):
    try:
        guests = int(message.text.replace('+', ''))
        if guests < 1 or guests > 20:
            raise ValueError()
    except ValueError:
        await message.answer('❌ Введите количество гостей (от 1 до 20).')
        return

    await state.update_data(guests=message.text)
    await message.answer('Есть ли предпочтения по размещению?', reply_markup=preferences_keyboard())
    await state.set_state(BookingState.preferences)


@router.message(BookingState.preferences)
async def get_preferences(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    date = data['date']
    time = data['time']
    guests = data['guests']
    preferences = message.text

    add_booking(user_id, date, time, guests, preferences)
    await state.clear()

    await message.answer(
        f'✅ Бронирование принято:\n📅 {date}\n🕒 {time}\n👥 {guests}\n💬 {preferences}\n\n'
        f'Если для брони требуется депозит — нажмите кнопку ниже:',
        reply_markup=payment_keyboard()
    )
