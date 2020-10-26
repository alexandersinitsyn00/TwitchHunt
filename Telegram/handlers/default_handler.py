from aiogram import types
from Telegram.misc import dp
from DataBaseManager.misc import db
from Telegram import states
from Twitch.misc import twitch_chat
from DataBaseManager.Exceptions import TelegramChatHasNoSubToChannel
import Twitch.TwitchDataParser as td
from Telegram.Exceptions import TwitchChannelNotValid

import sqlite3


@dp.message_handler()
async def echo(message: types.Message):
    chat_id = message['chat']['id']
    state = db.get_state_for_telegram_user(chat_id)

    # Обработка состояний
    if state == states.DOING_NOTHING:
        await message.answer('Пожалуйста, выберите команду')
    elif state == states.SUBSCRIBING:
        await subscribing(chat_id, message)
    elif state == states.UNSUBSCRIBING:
        await unsubscribing(chat_id, message)


async def subscribing(chat_id, message):
    try:
        channel_name = message.text.lower()

        if not await td.is_valid_channel(channel_name):
            raise TwitchChannelNotValid

        # Создать подписку
        db.add_subscription(chat_id, channel_name)

        # Подключиться к каналу
        await twitch_chat.add_channel(channel_name)

        await message.answer(f'Вы подписались на канал {message.text}')
        print(f'chat_id {chat_id} subscribed to channel {channel_name}')

        # Установить состояние канала - прослушивание
        db.set_state_for_twitch_channel(channel_name, 1)

    except sqlite3.IntegrityError:
        await message.reply('Вы уже подписаны на этот канал')

    except TwitchChannelNotValid:
        await message.reply('Канал с таким именем не найден, проверьте введенные данные')

    db.set_state_for_telegram_user(chat_id, states.DOING_NOTHING)


async def unsubscribing(chat_id, message):
    try:
        channel_name = message.text.lower()

        # Удалить подписку
        db.remove_subscription(chat_id, channel_name)

        await message.answer(f'Вы отписались от канала {message.text}')
        print(f'chat_id {chat_id} unsubscribed to channel {channel_name}')

        # Если подписчкиов это канала больше нет, покинуть канал и установить состояние канала в ноль
        if not db.is_channel_has_subscriptions(channel_name):
            await twitch_chat.remove_channel(channel_name)
            db.set_state_for_twitch_channel(channel_name, 0)
    except TelegramChatHasNoSubToChannel:
        await message.reply('Вы не были подписаны на этот канал')
    db.set_state_for_telegram_user(chat_id, states.DOING_NOTHING)
