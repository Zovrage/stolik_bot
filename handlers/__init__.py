from aiogram import Router

from .user_handler import router as user_router
from .payment import router as payment_router
from .booking import router as booking_router
from .InlineMode import router as inline_mode_router





router = Router()


router.include_routers(
    user_router, payment_router, booking_router, inline_mode_router
)