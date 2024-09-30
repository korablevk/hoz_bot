from aiogram import types
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from hozbot.dialogs.windows import main_window, input_window, pre_last_window, last_window, decorative_window, decorative_chicken_window

from aiogram_dialog import Dialog, DialogManager, Window, LaunchMode


bot_menu_dialogs = Dialog(
    main_window,
    input_window,
    pre_last_window,
    last_window,
    decorative_window,
    decorative_chicken_window,
    launch_mode=LaunchMode.ROOT,
)
