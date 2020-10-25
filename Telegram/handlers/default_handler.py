from aiogram import types
from Telegram.misc import dp
from DataBaseManager.misc import db
from Telegram import states
from Twitch.misc import twitch_chat
from DataBaseManager.Exceptions import TelegramChatHasNoSubToChannel
import sqlite3


@dp.message_handler()
async def echo(message: types.Message):
    chat_id = message['chat']['id']
    state = db.get_state_for_telegram_user(chat_id)
    if state == states.DOING_NOTHING:
        await message.answer('Пожалуйста, выберите команду')
    elif state == states.SUBSCRIBING:
        await subscribing(chat_id, message)
    elif state == states.UNSUBSCRIBING:
        await unsubscribing(chat_id, message)


async def subscribing(chat_id, message):
    try:
        db.add_subscription(chat_id, message.text)
        await twitch_chat.add_channel(message.text)
        await message.answer(f'Вы подписались на канал {message.text}')
        print(f'chat_id {chat_id} subscribed to channel {message.text}')
    except sqlite3.IntegrityError:
        await message.answer('Вы уже подписаны на этот канал')
    db.set_state_for_telegram_user(chat_id, states.DOING_NOTHING)


async def unsubscribing(chat_id, message):
    try:
        db.remove_subscription(chat_id, message.text)
        await message.answer(f'Вы отписались от канала {message.text}')
        print(f'chat_id {chat_id} unsubscribed to channel {message.text}')
        if not db.is_channel_has_subscriptions(message.text):
            await twitch_chat.remove_channel(message.text)
    except TelegramChatHasNoSubToChannel:
       await message.answer('Вы не были подписаны на этот канал')
    db.set_state_for_telegram_user(chat_id, states.DOING_NOTHING)
