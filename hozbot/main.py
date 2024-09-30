import asyncio
import ngrok
import uvicorn
from hozbot.bot import bot_main
from hozbot.logger import logger
from fastapi import FastAPI, Request
from sqladmin import Admin, ModelView
from hozbot.database.engine import engine
from hozbot.config import settings
from hozbot.models.birds_model import Birds
from contextlib import asynccontextmanager

# NGROK_AUTH_TOKEN = settings.NGROK_AUTHTOKEN
# NGROK_EDGE = settings.NGROK_EDGE
APPLICATION_PORT = 8000

# ngrok free tier only allows one agent. So we tear down the tunnel on application termination


app = FastAPI()
admin = Admin(app, engine)


class BirdAdmin(ModelView, model=Birds):
    column_list = [Birds.id, Birds.name, Birds.type_of_bird, Birds.cross_or_breed, Birds.meat_egg_complex, Birds.description]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = "Птица"
    name_plural = "Птицы"
    icon = "fa-solid fa-feather-pointed"


admin.add_view(BirdAdmin)


@app.get("/")
async def index(request: Request):
    return {"data": "Hello World"}


async def main():
    asyncio.create_task(bot_main())
    config = uvicorn.Config('main:app', host="0.0.0.0", port=8000, reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")