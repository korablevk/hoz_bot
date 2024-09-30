from aiogram_dialog import DialogManager


async def get_data_from_window(dialog_manager: DialogManager, **kwargs):
    return {
        "name": dialog_manager.find("name_input").get_value(),
        "bird_type": dialog_manager.find("bird_type_input").get_value().lower(),
        "cross_or_breed": dialog_manager.find("cross_or_breed_input").get_value().lower(),
        "meat_egg_complex": dialog_manager.find("meat_egg_complex_input").get_value().lower(),
        "description": dialog_manager.find("description_input").get_value(),
        "image_id": dialog_manager.dialog_data["image_id"],
    }