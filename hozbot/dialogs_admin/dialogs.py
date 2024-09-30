from aiogram_dialog import Window, Dialog, DialogManager, ShowMode, StartMode
from hozbot.dialogs_admin.windows import name_window, bird_type_window, cross_or_breed_window, meat_egg_complex_window, \
    description_window, image_id_window, last_window


dialog = Dialog(
    name_window,
    bird_type_window,
    cross_or_breed_window,
    meat_egg_complex_window,
    description_window,
    image_id_window,
    last_window,
    # price_window,
    # amount_window,  # here we specify data getter for dialog
)
