import asyncio
from os import environ
from os import path, curdir
from dotenv import load_dotenv

# Главный каталог
ROOT_DIR = path.abspath(curdir)

# Загрузить переменные виртуального окружения
dotenv_path = f'{ROOT_DIR}\\app\\application.env'
environ['ROOT_DIR'] = ROOT_DIR
load_dotenv(dotenv_path)

from Telegram import *
from .utils.TwitchController import add_twitch_tasks_to_event_loop


def run():
    loop = asyncio.get_event_loop()
    add_twitch_tasks_to_event_loop(loop)
    telegram.run(loop=loop)
