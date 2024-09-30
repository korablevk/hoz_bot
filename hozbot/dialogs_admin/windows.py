from aiogram.enums import ContentType
from aiogram.types import CallbackQuery

from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Group, Cancel
from aiogram_dialog.widgets.text import Const, Format
from aiogram import Router, types, F
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Radio, Column, Next, Back, StubScroll, NumberedPager
from aiogram_dialog.widgets.text import Const, Format, Jinja

from hozbot.dialogs_admin.getters import get_data_from_window
from hozbot.dialogs_admin.selected import error, next_window, on_input_photo, send_to_database
from hozbot.dialogs_admin.states import AddProduct
from hozbot.services.dao.birds_dao import BirdsDAO


name_window = Window(
    Const("Напишите название"),
    TextInput(id="name_input", filter=F.text, on_error=error, on_success=next_window),
    Cancel(Const("Отмена")),
    state=AddProduct.name,
)

bird_type_window = Window(
    Const("Напишите тип птицы курица, утка, перепела, индейка, гуси, цесарка, страус"),
    TextInput(id="bird_type_input", filter=F.text.lower().in_({"курица", "утка", "перепела", "индейка", "гуси",
                                                               "цесарка", "страус"}), on_error=error,
              on_success=Next()),
    Cancel(Const("Отмена")),
    Back(Const("Назад")),
    state=AddProduct.bird_type,
)

cross_or_breed_window = Window(
    Const("Напишите кросс, порода или декоративные"),
    TextInput(id="cross_or_breed_input", filter=F.text.lower().in_({"кросс", "порода", "декоративные"}), on_error=error,
              on_success=Next()),
    Cancel(Const("Отмена")),
    Back(Const("Назад")),
    state=AddProduct.cross_or_breed,
)

meat_egg_complex_window = Window(
    Const("Напишите мясные, яичные или мясояичные, или нету в случае декоративных"),
    TextInput(id="meat_egg_complex_input", filter=F.text.lower().in_({"мясные", "яичные", "мясояичные", "нету"}), on_error=error,
              on_success=Next()),
    Cancel(Const("Отмена")),
    Back(Const("Назад")),
    state=AddProduct.meat_egg_complex,
)

description_window = Window(
    Const("Напишите описание"),
    TextInput(id="description_input", filter=F.text, on_error=error,
              on_success=Next()),
    Cancel(Const("Отмена")),
    Back(Const("Назад")),
    state=AddProduct.description,
)

image_id_window = Window(
    Const("Отправьте фото"),
    Back(Const("Назад")),
    Cancel(Const("Отмена")),
    MessageInput(content_types=[ContentType.PHOTO], func=on_input_photo),
    state=AddProduct.image_id,
)

last_window = Window(
    Jinja(
        "<b>Название</b>: {{name}}, \n"
        "<b>Кросс или порода</b> {{cross_or_breed}} \n"
        "<b>Мясо, яйцо или микс</b>: {{meat_egg_complex}}\n"
        "<b>Описание</b>: {{description}}\n"
    ),
    Button(Const("Отправить в базу данных"), id="go", on_click=send_to_database),
    Back(Const("Назад")),
    Cancel(Const("Отмена")),
    state=AddProduct.send_database,
    getter=get_data_from_window
)
