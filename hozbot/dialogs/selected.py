from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from hozbot.dialogs.states import BotMenu, BuyProduct


# async def on_chosen_some_item(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
#     ctx = manager.current_context()
#     ctx.dialog_data.update(some_item=item_id)
#     await manager.switch_to(SomeGroupState.SomeAction)


async def on_chosen_type_of_bird(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(type_of_bird=item_id)
    await manager.switch_to(BotMenu.decorative)


async def get_back_to_(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(type_of_bird=item_id)
    await manager.switch_to(BotMenu.decorative)


async def on_chosen_product(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(product_id=item_id)
    await manager.switch_to(BotMenu.product_info)


async def on_buy_product(c: CallbackQuery, widget: Any, manager: DialogManager):
    ctx = manager.current_context()
    product_id = ctx.dialog_data.get('product_id')
    await manager.start(BuyProduct.enter_amount, data={'product_id': product_id})


# async def on_entered_amount(m: Message, widget: Any, manager: DialogManager, quantity: str):
#     ctx = manager.current_context()
#     session = manager.data.get('session')
#     if not quantity.isdigit():
#         await m.answer('Enter a number')
#         return
#
#     product_id = int(ctx.start_data.get('product_id'))
#     product_info = await repo.get_product(session, product_id)
#     stock = product_info.stock
#     if int(quantity) > stock:
#         await m.reply('Not enough in stock')
#         return
#
#     ctx.dialog_data.update(quantity=quantity)
#     await manager.switch_to(BuyProduct.confirm)


# async def on_confirm_buy(c: CallbackQuery, widget: Any, manager: DialogManager):
#     ctx = manager.current_context()
#     repo: Repo = manager.data.get('repo')
#     session = manager.data.get('session')
#
#     product_id = int(ctx.start_data.get('product_id'))
#     quantity = int(ctx.dialog_data.get('quantity'))
#
#     await repo.buy_product(session, product_id, quantity)
#     product = await repo.get_product(session, product_id)
#
#     await c.message.answer(f'You bought {quantity} {product.name}!')
#     await manager.done(result={'switch_to_window': SwitchToWindow.SelectProducts})