from aiogram import Router, Bot, Dispatcher, F
from aiogram.types import Message, WebAppInfo
from aiogram.filters import CommandStart, Command

from hozbot.filters.admin import IsAdmin
from hozbot.keyboards.inline import get_url_btns
from hozbot.config import settings


router = Router()
router.message.filter(IsAdmin())


@router.message(Command("panel"))
async def admin(message):
    await message.answer(
        text="Выберите птицу из ассортимента",
        reply_markup=get_url_btns(
            btns={
                "Админ панель": f"{settings.NGROK_TUNNEL_URL}/admin",
            },
        ),
    )

