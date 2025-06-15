from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from database.crud import is_time_available





class AvailabilityMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        state = data.get('state')
        if state:
            state_data = await state.get_data()
            date = state_data.get('date')
            time = state_data.get('time')

            if date and time and not is_time_available(date, time):
                await event.answer('❌ Это время уже занято. Пожалуйста, выберите другое.')
                return
        return await handler(event, data)