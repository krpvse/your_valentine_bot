import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from database import Database


# get env
load_dotenv('.env')
bot_token = os.getenv('BOT_TOKEN')
bot_name = os.getenv('BOT_NAME')
admin_id = os.getenv('ADMIN_ID')

# create telegram bot components
bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

# create database components
db = Database('database/sqlite3.db')
