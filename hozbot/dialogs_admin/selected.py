from typing import Any

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from hozbot.services.dao.birds_dao import BirdsDAO


async def error(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await manager.event.answer("Ошибка")


async def next_window(
        message: Message,
        dialog_: Any,
        dialog_manager: DialogManager,
        error_: ValueError
):
    await message.delete()
    await dialog_manager.next()


async def on_input_photo(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["image_id"] = message.photo[-1].file_id
    await dialog_manager.next()


async def send_to_database(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    try:
        await BirdsDAO.add(
            name=dialog_manager.find("name_input").get_value().lower(),
            type_of_bird=dialog_manager.find("bird_type_input").get_value().lower(),
            cross_or_breed=dialog_manager.find("cross_or_breed_input").get_value().lower(),
            meat_egg_complex=dialog_manager.find("meat_egg_complex_input").get_value().lower(),
            description=dialog_manager.find("description_input").get_value(),
            image_id=dialog_manager.dialog_data["image_id"],
        )
        await callback.answer("Товар добавлен")
        await dialog_manager.done()

    except Exception as e:
        await callback.answer(f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет")