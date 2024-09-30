from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import StartMode, ShowMode

from hozbot.dialogs.dialogs import bot_menu_dialogs
from hozbot.dialogs.states import BotMenu
from hozbot.lexicon.lexicon_ru import EXCEPTION

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Checkbox, Next, Radio, Row
from aiogram_dialog.widgets.text import Case, Const, Format
from typing import Any, Dict

dialog_router = Router()
dialog_router.include_routers(bot_menu_dialogs)


@dialog_router.message(Command('begin'))
async def begin(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(BotMenu.select_type_of_bird, show_mode=ShowMode.DELETE_AND_SEND, mode=StartMode.RESET_STACK)
    await message.delete()


@dialog_router.message()
async def start(message: Message):
    await message.answer(EXCEPTION['mistake'])