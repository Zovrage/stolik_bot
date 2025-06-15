import asyncio
import logging

from aiogram import Bot, Dispatcher

from database.db import create_table
from middleware.standart_middleware import AvailabilityMiddleware
from config import TOKEN
from handlers import router



async def main():
    create_table()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp.update.middleware.register(AvailabilityMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
    except Exception as ex:
        print(f'Ошибка: {ex}')