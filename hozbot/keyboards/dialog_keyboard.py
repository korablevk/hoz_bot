import operator

from aiogram_dialog.widgets.kbd import Select, ScrollingGroup
from aiogram_dialog.widgets.text import Format

SCROLLING_HEIGHT = 6


def paginated_products(on_click):
    return ScrollingGroup(
        Select(
            Format("{item.name}  pcs)"),
            id="s_scroll_products",
            item_id_getter=operator.attrgetter("product_id"),
            items="products",
            on_click=on_click,
        ),
        id="product_ids",
        width=1, height=SCROLLING_HEIGHT,
    )