from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from hozbot.lexicon.lexicon_ru import EXCEPTION, GREETING_TEXT, ABOUT_US_TEXT


router = Router()


@router.message(CommandStart())
@router.message(Command('help'))
async def start(message: Message):
    await message.delete()
    await message.answer(GREETING_TEXT['greeting'])


@router.message(Command('about'))
async def about(message: Message):
    await message.answer(ABOUT_US_TEXT['about'])


