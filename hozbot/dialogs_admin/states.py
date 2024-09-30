from aiogram.fsm.state import StatesGroup, State


class AddProduct(StatesGroup):
    name = State()
    bird_type = State()
    cross_or_breed = State()
    meat_egg_complex = State()
    description = State()
    image_id = State()
    send_database = State()
    price = State()
    amount = State()

    product_for_change = None

    texts = {
        'AddProduct:name': 'Введите название заново:',
        'AddProduct:bird_type': 'Введите bird_type заново:',
        'AddProduct:cross_or_breed': 'Введите cross_or_breed заново:',
        'AddProduct:meat_egg_complex': 'Введите meat_egg_complex заново:',
        'AddProduct:description': 'Введите описание заново:',
        'AddProduct:amount': 'Введите amount заново:',
        'AddProduct:price': 'Введите стоимость заново:',
        'AddProduct:image_id': 'Этот стейт последний, поэтому...',
    }