import asyncio

from aiogram import executor
from DataBaseManager.misc import db
from Twitch.misc import twitch_chat
from Telegram.misc import dp
import Telegram.handlers
import Twitch.TwitchDataParser as td


# Получение сообщений и сохранение в БД
async def save_twitch_messages():
    async for msg in twitch_chat.handle():
        db.save_twitch_message(msg['channel'], msg['user'], msg['msg'])


# Сохранение информации о стримах
async def save_stream_info():
    while True:
        listening_channels = db.get_list_of_listening_channels()
        for channel in listening_channels:
            stream_info = await td.get_stream_info_for_channel_if_streaming(channel)
            if stream_info is not None:
                db.save_stream_info(channel, stream_info['game_id'], stream_info['language'],
                                    stream_info['title'], stream_info['viewer_count'])
        await asyncio.sleep(60)


async def test_coroutine():
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(save_twitch_messages())
    loop.create_task(save_stream_info())

    # Запуск телеграмм бота и других задач с Event Loop
    executor.start_polling(dp, loop=loop)
