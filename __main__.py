import asyncio

from aiogram import executor
from DataBaseManager.misc import db
from Twitch.misc import twitch_chat
from Telegram.misc import dp
import Telegram.handlers


# Получение сообщений и сохранение в БД
async def run():
    async for msg in twitch_chat.handle():
        db.save_twitch_message(msg['channel'], msg['user'], msg['msg'])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(run())
    executor.start_polling(dp, loop=loop)
