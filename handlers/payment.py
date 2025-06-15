from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, PreCheckoutQuery, Message


from config import PAYMENTS_TOKEN

router = Router()


PRICE = [
    {
        'label': 'table',
        'amount': 50000
    }
]



@router.callback_query(F.data == 'pay_deposit')
async def handle_deposit(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title='Тестовая система оплаты Title',
        description='Описание тестовой системы оплаты',
        payload='Premium',
        provider_token=PAYMENTS_TOKEN,
        currency='RUB',
        prices=PRICE
    )



@router.pre_checkout_query()
async def checkout_cmd(query: PreCheckoutQuery):
    await query.answer(ok=True)



@router.message(lambda message: message.successful_payment is not None)
async def successful_payment_cmd(message: Message):
    await message.answer('Оплата прошла успешно')