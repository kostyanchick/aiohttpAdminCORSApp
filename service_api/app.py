import asyncio
import logging

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from service_api.config import Config

# this loop is used by application
loop = asyncio.get_event_loop()

logging.basicConfig(level=logging.DEBUG)

app = web.Application(loop=loop)
app.config = Config()

# connect and create db if not exist
mongo_client = AsyncIOMotorClient(app.config['MONGO_HOST'], app.config['MONGO_PORT'])
db = mongo_client[app.config['MONGO_DB_NAME']]





