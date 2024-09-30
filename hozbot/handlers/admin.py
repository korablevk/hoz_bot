from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode

from sqlalchemy.ext.asyncio import AsyncSession

from hozbot.dialogs_admin.dialogs import dialog
from hozbot.dialogs_admin.states import AddProduct
#
# from database.orm_query import (
#     orm_add_product,
#     orm_delete_product,
#     orm_get_product,
#     orm_get_products,
#     orm_update_product,
# )

from hozbot.filters.admin import IsAdmin
from hozbot.services.dao.birds_dao import BirdsDAO
from hozbot.keyboards.reply import get_keyboard
from hozbot.keyboards.inline import get_callback_btns


admin_router = Router()
admin_router.message.filter(IsAdmin())

ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент",
    placeholder="Выберите действие",
    sizes=(2,),
)


@admin_router.message(Command("admin"))
async def admin_features(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AddProduct.name, show_mode=ShowMode.DELETE_AND_SEND, mode=StartMode.RESET_STACK)
    await message.delete()


admin_router.include_router(dialog)











#
# admin_router = Router()
# admin_router.message.filter(IsAdmin())
#
# ADMIN_KB = get_keyboard(
#     "Добавить товар",
#     "Ассортимент",
#     placeholder="Выберите действие",
#     sizes=(2,),
# )
#
#
# @admin_router.message(Command("admin"))
# async def admin_features(message: types.Message):
#     await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)
#
#
# class AddProduct(StatesGroup):
#     # Шаги состояний
#     name = State()
#     bird_type = State()
#     cross_or_breed = State()
#     meat_egg_complex = State()
#     description = State()
#     characteristics = State()
#     image_id = State()
#     price = State()
#     amount = State()
#
#     product_for_change = None
#
#     texts = {
#         'AddProduct:name': 'Введите название заново:',
#         'AddProduct:bird_type': 'Введите bird_type заново:',
#         'AddProduct:cross_or_breed': 'Введите cross_or_breed заново:',
#         'AddProduct:meat_egg_complex': 'Введите meat_egg_complex заново:',
#         'AddProduct:description': 'Введите описание заново:',
#         'AddProduct:characteristics': 'Введите characteristics заново:',
#         'AddProduct:amount': 'Введите amount заново:',
#         'AddProduct:price': 'Введите стоимость заново:',
#         'AddProduct:image_id': 'Этот стейт последний, поэтому...',
#     }
#
#
# @admin_router.message(F.text == "Ассортимент")
# async def starring_at_product(message: types.Message):
#     await message.answer(
#             text="Выберите птицу из ассортимента",
#             reply_markup=get_callback_btns(
#                 btns={
#                     "Курица": "курица",
#                     "Утка": "утка",
#                     "Перепелка": "перепелка",
#                 },
#             ),
#         )
#
#
# @admin_router.callback_query(F.data.in_({"курица", "утка", "перепела"}))
# async def send_product_callback(callback: types.CallbackQuery):
#     bird_type = str(callback.data)
#     await callback.message.answer(text=f"Ассортимент {bird_type}:", reply_markup=types.ReplyKeyboardRemove())
#     products = await BirdsDAO.find_birds(type_of_bird=bird_type)
#     for product in products:
#         await callback.message.answer_photo(
#             product.image_id,
#             caption=f"<strong>{product.name}\
#                         </strong>\n{product.description}\nСтоимость:",
#             reply_markup=get_callback_btns(
#                 btns={
#                     "Удалить": f"delete_{product.id}",
#                     "Изменить": f"change_{product.id}",
#                 }
#             ),
#         )
#
#
# @admin_router.callback_query(F.data.startswith("delete_"))
# async def delete_product_callback(callback: types.CallbackQuery, session: AsyncSession):
#     product_id = callback.data.split("_")[-1]
#     await BirdsDAO.delete_bird(int(product_id))
#
#     await callback.answer("Товар удален")
#     await callback.message.answer("Товар удален!")
#
#
# @admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
# async def change_product_callback(
#     callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
# ):
#     product_id = callback.data.split("_")[-1]
#
#     product_for_change = await BirdsDAO.find_by_id(int(product_id))
#
#     AddProduct.product_for_change = product_for_change
#
#     await callback.answer()
#     await callback.message.answer(
#         "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
#     )
#     await state.set_state(AddProduct.name)
#
#
# # Становимся в состояние ожидания ввода name
# @admin_router.message(StateFilter(None), F.text == "Добавить товар")
# async def add_product(message: types.Message, state: FSMContext):
#     await message.answer(
#         "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
#     )
#     await state.set_state(AddProduct.name)
#
#
# # Хендлер отмены и сброса состояния должен быть всегда именно хдесь,
# # после того как только встали в состояние номер 1 (элементарная очередность фильтров)
# @admin_router.message(StateFilter('*'), Command("отмена"))
# @admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
# async def cancel_handler(message: types.Message, state: FSMContext) -> None:
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#
#     await state.clear()
#     await message.answer("Действия отменены", reply_markup=ADMIN_KB)
#
#
# # Вернутся на шаг назад (на прошлое состояние)
# @admin_router.message(StateFilter('*'), Command("назад"))
# @admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
# async def back_step_handler(message: types.Message, state: FSMContext) -> None:
#     current_state = await state.get_state()
#
#     if current_state == AddProduct.name:
#         await message.answer('Предидущего шага нет, или введите название товара или напишите "отмена"')
#         return
#
#     previous = None
#     for step in AddProduct.__all_states__:
#         if step.state == current_state:
#             await state.set_state(previous)
#             await message.answer(f"Ок, вы вернулись к прошлому шагу \n {AddProduct.texts[previous.state]}")
#             return
#         previous = step
#
#
# @admin_router.message(AddProduct.name, or_f(F.text, F.text == "."))
# async def add_name(message: types.Message, state: FSMContext):
#     # Здесь можно сделать какую либо дополнительную проверку
#     # и выйти из хендлера не меняя состояние с отправкой соответствующего сообщения
#     # например:
#     if message.text == ".":
#         await state.update_data(name=AddProduct.product_for_change.name)
#     else:
#         if len(message.text) >= 100:
#             await message.answer("Название товара не должно превышать 100 символов.\n Введите заново")
#             return
#
#         await state.update_data(name=message.text)
#     await message.answer("Введите тип птицы\nКурица,утка,перепела")
#     await state.set_state(AddProduct.bird_type)
#
#
# # Хендлер для отлова некорректных вводов для состояния name
# @admin_router.message(AddProduct.name)
# async def add_name2(message: types.Message, state: FSMContext):
#     await message.answer("Вы ввели не допустимые данные, введите текст названия товара")
#
#
# @admin_router.message(AddProduct.bird_type, or_f(F.text.lower().in_({"курица", "утка", "перепела"}), F.text == "."))
# async def add_bird_type(message: types.Message, state: FSMContext):
#     if message.text == ".":
#         await state.update_data(bird_type=AddProduct.product_for_change.type_of_bird)
#     else:
#         await state.update_data(bird_type=message.text.lower())
#     await message.answer("Введите порода или кросс")
#     await state.set_state(AddProduct.cross_or_breed)
#
#
# # Хендлер для отлова некорректных вводов для состояния name
# @admin_router.message(AddProduct.bird_type)
# async def add_bird_type2(message: types.Message, state: FSMContext):
#     await message.answer("Введите тип птицы\nКурица,утка,перепела")
#
#
# @admin_router.message(AddProduct.cross_or_breed, or_f(F.text.lower().in_({"порода", "кросс"}), F.text == "."))
# async def add_cross_or_breed(message: types.Message, state: FSMContext):
#     if message.text == ".":
#         await state.update_data(cross_or_breed=AddProduct.product_for_change.cross_or_breed)
#     else:
#         await state.update_data(cross_or_breed=message.text.lower())
#     await message.answer("Порода или кросс выбран\nВыберите мясо,яйцо или микс")
#     await state.set_state(AddProduct.meat_egg_complex)
#
#
# @admin_router.message(AddProduct.cross_or_breed)
# async def add_cross_or_breed2(message: types.Message, state: FSMContext):
#     await message.answer("cross_or_breed33 пищи")
#
#
# @admin_router.message(AddProduct.meat_egg_complex, or_f(F.text.lower().in_({"мясо", "яйцо", "микс"}), F.text == "."))
# async def add_meat_egg_complex(message: types.Message, state: FSMContext):
#     if message.text == ".":
#         await state.update_data(meat_egg_complex=AddProduct.product_for_change.meat_egg_complex)
#     else:
#         await state.update_data(meat_egg_complex=message.text.lower())
#     await message.answer("Мясо,яйцо или микс выбран\nНапишите описание товара")
#     await state.set_state(AddProduct.description)
#
#
# @admin_router.message(AddProduct.meat_egg_complex)
# async def add_meat_egg_complex2(message: types.Message, state: FSMContext):
#     await message.answer("meat_egg_complex44 пищи")
#
#
# # Ловим данные для состояние description и потом меняем состояние на price
# @admin_router.message(AddProduct.description, or_f(F.text, F.text == "."))
# async def add_description(message: types.Message, state: FSMContext):
#     if message.text == ".":
#         await state.update_data(description=AddProduct.product_for_change.description)
#     else:
#         await state.update_data(description=message.text)
#     await message.answer("Введите характеристики товара через запятую\nЕсли нет то напишите 'нет'")
#     await state.set_state(AddProduct.characteristics)
#
#
# # Хендлер для отлова некорректных вводов для состояния description
# @admin_router.message(AddProduct.description)
# async def add_description2(message: types.Message, state: FSMContext):
#     await message.answer("Вы ввели не допустимые данные, введите текст описания товара")
#
#
# @admin_router.message(AddProduct.characteristics, or_f(F.text, F.text == "."))
# async def add_characteristics(message: types.Message, state: FSMContext):
#     if message.text == ".":
#         await state.update_data(description=AddProduct.product_for_change.description)
#     else:
#         await state.update_data(characteristics=list(message.text.split(',')) if message.text != 'нет' else "отсутвуют")
#     await message.answer("Напишите цену товара")
#     await state.set_state(AddProduct.price)
#
#
# # Хендлер для отлова некорректных вводов для состояния description
# @admin_router.message(AddProduct.characteristics)
# async def add_characteristics2(message: types.Message, state: FSMContext):
#     await message.answer("Вы ввели не допустимые данные, введите текст описания товара")
#
#
# # Ловим данные для состояние price и потом меняем состояние на image
# @admin_router.message(AddProduct.price, F.text)
# async def add_price(message: types.Message, state: FSMContext):
#     if message.text == "." and AddProduct.product_for_change:
#         await state.update_data(price=AddProduct.product_for_change.price)
#     else:
#         try:
#             float(message.text)
#         except ValueError:
#             await message.answer("Введите корректное значение цены")
#             return
#
#         await state.update_data(price=message.text)
#     await message.answer("Напиши количество товара")
#     await state.set_state(AddProduct.amount)
#
#
# # Хендлер для отлова некорректных ввода для состояния price
# @admin_router.message(AddProduct.price)
# async def add_price2(message: types.Message, state: FSMContext):
#     await message.answer("Вы ввели не допустимые данные, введите стоимость товара")
#
#
# @admin_router.message(AddProduct.amount, F.text)
# async def add_price(message: types.Message, state: FSMContext):
#     if message.text == "." and AddProduct.product_for_change:
#         await state.update_data(price=AddProduct.product_for_change.amount)
#     else:
#         try:
#             int(message.text)
#         except ValueError:
#             await message.answer("Введите корректное значение цены")
#             return
#
#         await state.update_data(price=message.text)
#     await message.answer("Напиши количество товара")
#     await state.set_state(AddProduct.image_id)
#
#
# @admin_router.message(AddProduct.amount)
# async def add_price2(message: types.Message, state: FSMContext):
#     await message.answer("Вы ввели не допустимые данные, введите стоимость товара")
#
#
# @admin_router.message(AddProduct.image_id, or_f(F.photo, F.text == "."))
# async def add_image(message: types.Message, state: FSMContext):
#     if message.text and message.text == ".":
#         await state.update_data(image_id=AddProduct.product_for_change.image_id)
#
#     else:
#         await state.update_data(image_id=message.photo[-1].file_id)
#     data = await state.get_data()
#     try:
#         if AddProduct.product_for_change:
#             await BirdsDAO.update_bird(AddProduct.product_for_change.id, data)
#         else:
#             await BirdsDAO.add(
#                 name=data["name"],
#                 type_of_bird=data["bird_type"],
#                 cross_or_breed=data["cross_or_breed"],
#                 meat_egg_complex=data["meat_egg_complex"],
#                 description=data["description"],
#                 characteristics=data["characteristics"],
#                 image_id=data["image_id"],
#             )
#         await message.answer("Товар добавлен/изменен", reply_markup=ADMIN_KB)
#         await state.clear()
#
#     except Exception as e:
#         await message.answer(
#             f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет",
#             reply_markup=ADMIN_KB,
#         )
#         await state.clear()
#
#     AddProduct.product_for_change = None
#
#
# @admin_router.message(AddProduct.image_id)
# async def add_image2(message: types.Message, state: FSMContext):
#     await message.answer("Отправьте фото")