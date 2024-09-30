from sqlalchemy.exc import SQLAlchemyError

from hozbot.logger import logger
from hozbot.models.birds_model import Birds
from hozbot.services.dao.base import BaseDAO
from hozbot.database.engine import async_session_maker

from sqlalchemy import select, delete, update, and_


class BirdsDAO(BaseDAO):
    model = Birds

    @classmethod
    async def find_birds(cls, type_of_bird: str):
        async with async_session_maker() as session:
            query = (select(Birds).where(Birds.type_of_bird == type_of_bird))
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def delete_bird(cls, product_id: int):
        async with async_session_maker() as session:
            query = (delete(Birds).where(Birds.id == product_id))
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_bird(cls, product_id: int, data):
        async with async_session_maker() as session:
            query = update(Birds).where(Birds.id == product_id).values(
                name=data["name"],
                type_of_bird=data["bird_type"],
                cross_or_breed=data["cross_or_breed"],
                meat_egg_complex=data["meat_egg_complex"],
                description=data["description"],
                image_id=data["image_id"],
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def user_select(cls,
                          type_of_bird: str,
                          cross_or_breed: str,
                          meat_egg_complex: str):
        try:
            async with (async_session_maker() as session):
                query = (
                    select(Birds)
                    .where(
                        and_(Birds.type_of_bird == type_of_bird, Birds.cross_or_breed == cross_or_breed,
                             Birds.meat_egg_complex == meat_egg_complex)))
                result = await session.execute(query)
                return result.scalars().all()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot find bird"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot find bird"
            extra = {
                "type_of_bird": type_of_bird,
                "cross_or_breed": cross_or_breed,
                "meat_egg_complex": meat_egg_complex,
            }
            logger.error(msg, extra=extra, exc_info=True)
