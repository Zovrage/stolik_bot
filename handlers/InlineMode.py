from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4

from database.crud import get_user_bookings

router = Router()


@router.inline_query()
async def inline_bookings(query: InlineQuery):
    user_id = query.from_user.id
    bookings = get_user_bookings(user_id)

    results = []

    if not bookings:
        results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Нет активных бронирований",
                input_message_content=InputTextMessageContent(
                    message_text="У вас нет активных бронирований."
                )
            )
        )
    else:
        for b in bookings:
            booking_text = (
                f"🍽 Бронирование\n"
                f"📅 Дата: {b[2]}\n"
                f"🕒 Время: {b[3]}\n"
                f"👥 Гостей: {b[4]}\n"
                f"💬 Предпочтения: {b[5]}\n"
                f"{'✅ Оплачено' if b[6] else '❌ Не оплачено'}"
            )

            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=f"{b[2]} {b[3]} | {b[4]} чел.",
                    input_message_content=InputTextMessageContent(
                        message_text=booking_text
                    )
                )
            )

    await query.answer(results, cache_time=1)

