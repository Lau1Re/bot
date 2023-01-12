import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from dotenv import load_dotenv

load_dotenv()

PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_USER = os.getenv('PROXY_LOGIN')
PROXY_PASS = os.getenv('PROXY_PASSWORD')
TOKEN = os.getenv('API_TOKEN')
DATABASE = 'database.sqlite3'

bot = Bot(TOKEN, parse_mode='HTML')
storage = RedisStorage2()
loop = asyncio.get_event_loop()

dp = Dispatcher(bot, loop=loop, storage=storage)
