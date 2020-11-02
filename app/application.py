from pathlib import Path
import asyncio
from os import environ
from os import path, curdir
from dotenv import load_dotenv



# Загрузить переменные виртуального окружения
dotenv_path = Path.cwd() / 'app' / 'application.env'
load_dotenv(dotenv_path)

from Telegram import *
from .utils.TwitchController import add_twitch_tasks_to_event_loop


def run():
    loop = asyncio.get_event_loop()
    add_twitch_tasks_to_event_loop(loop)
    telegram.run(loop=loop)
