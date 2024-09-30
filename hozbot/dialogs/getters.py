from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from hozbot.lexicon.lexicon_ru import CATEGORIES
from hozbot.dialogs.states import BotMenu
from hozbot.logger import logger
from hozbot.services.dao.birds_dao import BirdsDAO

TYPE_OF_BIRD_ID = "tob"
TYPE_OF_DECORATIVE_BIRD_ID = "todb"
DECORATIVE_BIRDS = 'db'
CROSS_OR_BREED_ID = "cob"
MEAT_EGG_COMPLEX_ID = "mec"
ID_STUB_SCROLL = "stub_scroll"
ID_DECORATIVE_STUB_SCROLL = "stub_scroll2"


async def get_products(dialog_manager: DialogManager, **middleware_data):
    type_of_bird = str(dialog_manager.find(TYPE_OF_BIRD_ID).get_checked()).lower()
    cross_or_breed = str(dialog_manager.find(CROSS_OR_BREED_ID).get_checked()).lower()
    meat_egg_complex = str(dialog_manager.find(MEAT_EGG_COMPLEX_ID).get_checked()).lower()

    if not type_of_bird:
        await dialog_manager.event.answer('В начале выберите тип птицы')
        await dialog_manager.switch_to(BotMenu.select_type_of_bird)
        return
    elif not cross_or_breed:
        await dialog_manager.event.answer('В начале выберите кросс или порода')
        await dialog_manager.switch_to(BotMenu.select_cross_or_breed)
        return
    elif not meat_egg_complex:
        await dialog_manager.event.answer('В начале выберите мясо, яйцо или микс')
        await dialog_manager.switch_to(BotMenu.select_meat_egg_or_complex)
        return

    db_products = await BirdsDAO.user_select(type_of_bird=type_of_bird, cross_or_breed=cross_or_breed,
                                             meat_egg_complex=meat_egg_complex)
    if db_products:
        try:
            current_page = await dialog_manager.find(ID_STUB_SCROLL).get_page()
            cnt_products = len(db_products)
            current_product = db_products[current_page]
            dialog_manager.dialog_data["id"] = current_product.id
            return {
                "name": current_product.name.title(),
                "type_of_bird": current_product.type_of_bird.title(),
                "cross_or_breed": current_product.cross_or_breed.title(),
                "meat_egg_complex": current_product.meat_egg_complex.title(),
                "description": current_product.description,
                "current_page": current_page + 1,
                "cnt_products": cnt_products,
                "photo": MediaAttachment(ContentType.PHOTO, file_id=MediaId(current_product.image_id))
            }
        except Exception:
            await dialog_manager.event.answer('Произошла ошибка')
            logger.error(f"Ошибка:{Exception}")
    else:
        await dialog_manager.event.answer('Отсутвует в базе данных')
        logger.error("Нет данных в базе данных")


async def get_decorative_products(dialog_manager: DialogManager, **middleware_data):
    type_of_bird = str(dialog_manager.find(DECORATIVE_BIRDS).get_checked()).lower()
    cross_or_breed = str(dialog_manager.find(TYPE_OF_DECORATIVE_BIRD_ID).get_checked()).lower()
    meat_egg_complex = 'нету'

    if not type_of_bird:
        await dialog_manager.event.answer('В начале выберите тип птицы')
        await dialog_manager.switch_to(BotMenu.select_type_of_bird)
        return
    elif not cross_or_breed:
        await dialog_manager.event.answer('В начале выберите кросс или порода')
        await dialog_manager.switch_to(BotMenu.select_cross_or_breed)
        return

    db_products = await BirdsDAO.user_select(type_of_bird=type_of_bird, cross_or_breed=cross_or_breed,
                                             meat_egg_complex=meat_egg_complex)

    print(type_of_bird, cross_or_breed, meat_egg_complex)

    print(db_products)

    if db_products:
        try:
            current_page = await dialog_manager.find(ID_DECORATIVE_STUB_SCROLL).get_page()
            cnt_products = len(db_products)
            current_product = db_products[current_page]
            dialog_manager.dialog_data["id"] = current_product.id
            return {
                "name": current_product.name.title(),
                "type_of_bird": current_product.type_of_bird.title(),
                "description": current_product.description,
                "current_page": current_page + 1,
                "cnt_products": cnt_products,
                "photo": MediaAttachment(ContentType.PHOTO, file_id=MediaId(current_product.image_id))
            }
        except Exception:
            await dialog_manager.event.answer('Произошла ошибка')
            logger.error(f"Ошибка:{Exception}")
    else:
        await dialog_manager.event.answer('Отсутвует в базе данных')
        logger.error("Нет данных в базе данных")
