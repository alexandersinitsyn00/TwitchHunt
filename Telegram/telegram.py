import asyncio
from os import environ
from aiogram import Bot, Dispatcher, executor, types

token = environ.get("TG_TOKEN")
bot = Bot(token)
dp = Dispatcher(bot)


def run(loop):
    executor.start_polling(dp, loop=loop, skip_updates=True)
