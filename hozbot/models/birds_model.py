from typing import TYPE_CHECKING

from sqlalchemy import String, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hozbot.database.engine import Base


class Birds(Base):
    __tablename__ = "birds"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    type_of_bird: Mapped[str] = mapped_column(String, nullable=False)
    cross_or_breed: Mapped[str] = mapped_column(String, nullable=True)
    meat_egg_complex: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(Text)
    image_id: Mapped[int] = mapped_column(String)

    def __str__(self):
        return f"Птица {self.name}"