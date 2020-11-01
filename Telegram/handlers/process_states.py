import sqlite3
from aiogram import types

import Twitch.TwitchDataParser as td
from DataBase import *
from DataBase.Engine import Exceptions as DbExceptions
from ..telegram import dp
from .. import states


@dp.message_handler()
async def echo(message: types.Message):
    chat_id = message['chat']['id']
    state = db.get_state_for_tg_chat(chat_id)

    # Обработка состояний
    if state == states.DOING_NOTHING:
        await message.answer('Пожалуйста, выберите команду')
    elif state == states.SUBSCRIBING:
        await subscribing(chat_id, message)
    elif state == states.UNSUBSCRIBING:
        await unsubscribing(chat_id, message)


async def subscribing(chat_id, message):
    db.set_state_for_tg_chat(chat_id, states.DOING_NOTHING)

    channel_name = message.text.lower()

    if not await td.is_valid_channel(channel_name):
        await message.reply('Канал с таким именем не найден, проверьте введенные данные')
        return

    # Создать подписку
    try:
        db.add_tw_subscription(chat_id, channel_name)
    except DbExceptions.TgChatIsNotSubscribedToTwChannel:
        await message.answer(f'Вы уже подписаны на канал {message.text}')
        return

    await message.answer(f'Вы подписались на канал {message.text}')
    print(f'chat_id {chat_id} subscribed to channel {channel_name}')


async def unsubscribing(chat_id, message):
    channel_name = message.text.lower()

    # Удалить подписку
    try:
        db.remove_tw_subscription(chat_id, channel_name)
    except DbExceptions.TgChatIsNotSubscribedToTwChannel:
        await message.answer(f'Вы не были подписаны на канал {message.text}')
        return

    await message.answer(f'Вы отписались от канала {message.text}')
    print(f'chat_id {chat_id} unsubscribed to channel {channel_name}')

    db.set_state_for_tg_chat(chat_id, states.DOING_NOTHING)
