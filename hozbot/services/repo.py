from aiocache import Cache
from sqlalchemy.ext.asyncio import AsyncSession

from hozbot.services.dao.birds_dao import BirdsDAO


class Repo:
    def __init__(self, session: AsyncSession, cache: Cache = None):
        self.session = session
        # self.bird_dao = BirdsDAO(session=session)
