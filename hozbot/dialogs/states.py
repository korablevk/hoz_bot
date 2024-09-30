from aiogram.filters.state import State, StatesGroup


class BotMenu(StatesGroup):
    select_type_of_bird = State()
    select_cross_or_breed = State()
    select_meat_egg_or_complex = State()
    product_info = State()
    decorative = State()
    decorative_product_info = State()


class BuyProduct(StatesGroup):
    enter_amount = State()
    confirm = State()
