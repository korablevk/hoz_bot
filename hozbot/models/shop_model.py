from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, Float, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hozbot.database.engine import Base


if TYPE_CHECKING:
    from hozbot.models.birds_model import Birds


class Shop(Base):
    __tablename__ = "shop"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Float(asdecimal=True), nullable=False)
    bird_id: Mapped[int] = mapped_column(ForeignKey('birds.id', ondelete='CASCADE'), nullable=False)

    bird: Mapped["Birds"] = relationship(backref='shop')

    def __str__(self):
        return f"Товар {self.id}"


# class User(Base):
#     __tablename__ = 'user'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
#     first_name: Mapped[str] = mapped_column(String(), nullable=True)
#     last_name: Mapped[str] = mapped_column(String(), nullable=True)
#     phone: Mapped[str] = mapped_column(String(), nullable=True)
#     telegram_id: Mapped[str] = mapped_column(String(), nullable=True)
#
#     def __str__(self):
#         return f"Пользователь {self.first_name}"
#
#
# class Order(Base):
#     __tablename__ = 'order'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
#     bird_id: Mapped[int] = mapped_column(ForeignKey('birds.id', ondelete='CASCADE'), nullable=False)
#     quantity: Mapped[int]
#
#     user: Mapped['User'] = relationship(backref='order')
#     bird: Mapped['Birds'] = relationship(backref='order')
#
#     def __str__(self):
#         return f"Заказ {self.id}"