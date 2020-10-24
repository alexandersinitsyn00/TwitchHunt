import logging
from aiogram import Bot, Dispatcher

bot = Bot(token="1195418865:AAEUWthgwgQCWNxCU4zir62hrm7zc5XQmu8")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)