import asyncio
from datetime import datetime

from aiogram import executor
from DataBaseManager.misc import db
from Twitch.misc import twitch_chat
from Telegram.misc import dp
import Telegram.handlers


# Получение сообщений и сохранение в БД
async def run():
    async for msg in twitch_chat.handle():
        db.save_twitch_message(msg['channel'], msg['user'], msg['msg'])


# TEST
async def test_coroutine():
    while True:
        print(db.VIEW_MESSAGES_COUNT_PER_MINUTE_FOR_CHANNEL('manyrin'))
        await asyncio.sleep(10)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(run())
    loop.create_task(test_coroutine())
    executor.start_polling(dp, loop=loop)
