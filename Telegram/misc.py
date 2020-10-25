import logging
from aiogram import Bot, Dispatcher
from Settings.misc import settings

bot = Bot(token=settings.get_telegram_token())
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
