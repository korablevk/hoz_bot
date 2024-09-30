from dataclasses import dataclass
from typing import Dict, Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, Window, ChatEvent
from aiogram_dialog.widgets.common import ManagedScroll, Whenable
from aiogram_dialog.widgets.kbd import Radio, Column, Next, Back, StubScroll, NumberedPager, Button, ManagedRadio
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Jinja

from hozbot.config import settings
from hozbot.dialogs.getters import get_products, get_decorative_products, TYPE_OF_BIRD_ID, ID_STUB_SCROLL, \
    CROSS_OR_BREED_ID, MEAT_EGG_COMPLEX_ID, TYPE_OF_DECORATIVE_BIRD_ID, DECORATIVE_BIRDS, ID_DECORATIVE_STUB_SCROLL
from hozbot.dialogs.selected import on_chosen_type_of_bird
from hozbot.dialogs.states import BotMenu
from hozbot.filters.admin import IsAdmin
from hozbot.services.dao.birds_dao import BirdsDAO

HEADER = Const("Выберите опцию снизу:\n")


@dataclass
class Bird:
    id: str
    name: str


async def on_delete(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, **kwargs):
    product_id = int(dialog_manager.dialog_data["id"])
    if product_id:
        await BirdsDAO.delete_bird(product_id)
        await callback.answer("Продукт удален")
        await dialog_manager.back()
    else:
        await callback.answer("Ошибка")


def is_admin(data: Dict, widget: Whenable, dialog_manager: DialogManager):
    return dialog_manager.event.from_user.id in settings.ADMINS


async def change_on_decorative_birds(data: Dict, widget: Radio, dialog_manager: DialogManager):
    await dialog_manager.switch_to(BotMenu.decorative)


async def get_back_to_first_window(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    ...  # your actions
    await dialog_manager.switch_to(BotMenu.select_type_of_bird)


main_window = Window(
    HEADER,
    Const("Шаг 1. Выберите опцию"),
    Column(
        Radio(
            checked_text=Format("🔘 {item}"),
            unchecked_text=Format("⚪️ {item}"),
            items=["Курица", "Перепелка", "Индейка", "Утка", "Гуси", "Цесарка"],
            item_id_getter=lambda x: x,
            id=TYPE_OF_BIRD_ID,
            on_click=Next(),
        ),
        Radio(
            checked_text=Format("🔘 {item}"),
            unchecked_text=Format("⚪️ {item}"),
            items=["Декоративные"],
            item_id_getter=lambda x: x,
            id=TYPE_OF_DECORATIVE_BIRD_ID,
            on_click=on_chosen_type_of_bird,
        ),
    ),
    state=BotMenu.select_type_of_bird,
)

input_window = Window(
    HEADER,
    Const("Шаг 2. Выберите опцию"),
    Column(
        Radio(
            checked_text=Format("🔘 {item}"),
            unchecked_text=Format("⚪️ {item}"),
            items=["Порода", "Кросс"],
            item_id_getter=lambda x: x,
            id=CROSS_OR_BREED_ID,
            on_click=Next()
        ),
        Back(Const('Назад')),
    ),
    state=BotMenu.select_cross_or_breed,
)

pre_last_window = Window(
    HEADER,
    Const("Шаг 3. Выберите опцию"),
    Column(
        Radio(
            checked_text=Format("🔘 {item}"),
            unchecked_text=Format("⚪️ {item}"),
            items=["Мясные", "Яичные", "Мясояичные"],
            item_id_getter=lambda x: x,
            id=MEAT_EGG_COMPLEX_ID,
            on_click=Next(),
        ),
        Back(Const('Назад')),
    ),
    state=BotMenu.select_meat_egg_or_complex,
)

last_window = Window(
    Jinja(
        "<b>Название</b>: {{name}}, {{cross_or_breed}} \n"
        "<b>Тип птицы</b>: {{meat_egg_complex}}\n"
        "<b>Описание</b>: {{description}}\n"
    ),
    DynamicMedia("photo"),
    Button(
        Const("Удалить"),
        id="del",
        on_click=on_delete,
        when=is_admin,
    ),
    Column(StubScroll(id=ID_STUB_SCROLL, pages="cnt_products")),
    NumberedPager(scroll=ID_STUB_SCROLL),
    Back(Const('Назад')),
    state=BotMenu.product_info,
    getter=get_products,
    preview_data=get_products,
)

decorative_window = Window(
    HEADER,
    Const("Шаг 2. Выберите опцию"),
    Column(
        Radio(
            checked_text=Format("🔘 {item}"),
            unchecked_text=Format("⚪️ {item}"),
            items=["Курица", "Страус"],
            item_id_getter=lambda x: x,
            id=DECORATIVE_BIRDS,
            on_click=Next(),
        ),
        Button(Const("Назад"),
               id="to_first_window",
               on_click=get_back_to_first_window),
    ),
    state=BotMenu.decorative,
)

decorative_chicken_window = Window(
    Jinja(
        "<b>Название</b>: {{name}}, {{cross_or_breed}} \n"
        "<b>Описание</b>: {{description}}\n"
    ),
    DynamicMedia("photo"),
    Button(
        Const("Удалить"),
        id="del",
        on_click=on_delete,
        when=is_admin,
    ),
    Column(StubScroll(id=ID_DECORATIVE_STUB_SCROLL, pages="cnt_products")),
    NumberedPager(scroll=ID_DECORATIVE_STUB_SCROLL),
    Back(Const('Назад')),
    state=BotMenu.decorative_product_info,
    getter=get_decorative_products,
    preview_data=get_decorative_products,
)
