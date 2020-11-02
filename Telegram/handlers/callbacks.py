from os import environ
from pathlib import Path
from datetime import datetime as dt
from .. import states
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..telegram import dp
from ..telegram import bot

from DataBase import *
from DataBase.Engine import Exceptions as DbExceptions
from GraphicBuilder.GraphicBuilder import *

data_path = Path.cwd() / environ.get("DATA_DIR")

VIEW_MSG_QTY = 'Кол-во сообщений'
VIEW_VIWERS_COUNT_QTY = 'Кол-во зрителей'
UNSUB = 'Отписаться'

actions = [
    UNSUB,
    VIEW_MSG_QTY
]


# channel callback
@dp.callback_query_handler(lambda query: query.data.startswith('channel:'))
async def process_channel_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    channel = callback_query.data.replace('channel:', '')
    act_keyboard = InlineKeyboardMarkup(row_width=2)
    for act in actions:
        btn = InlineKeyboardButton(act, callback_data=f'act:{act}*channel:{channel}')
        act_keyboard.insert(btn)
    await bot.send_message(callback_query.from_user.id,
                           f'Выберите опцию для канала {channel}',
                           reply_markup=act_keyboard)


# action for channel callback
@dp.callback_query_handler(lambda query: query.data.startswith('act:'))
async def process_action_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    chat_id = callback_query.message.chat.id

    data = callback_query.data.replace('act:', '').replace('channel:', '').split('*')
    act = data[0]
    channel = data[1]
    if act == VIEW_MSG_QTY:
        await create_send_qty_msg_graph(chat_id, channel)
    elif act == UNSUB:
        await unsubscribing(chat_id, channel)


async def unsubscribing(chat_id, channel_name):
    # Удалить подписку
    try:
        db.remove_tw_subscription(chat_id, channel_name)
    except DbExceptions.TgChatIsNotSubscribedToTwChannel:
        await bot.send_message(chat_id, f'Вы не были подписаны на канал {channel_name}')
        return

    await bot.send_message(chat_id, f'Вы отписались от канала {channel_name}')
    print(f'chat_id {chat_id} unsubscribed to channel {channel_name}')

    db.set_state_for_tg_chat(chat_id, states.DOING_NOTHING)


async def create_send_qty_msg_graph(chat_id, channel_name):
    try:
        file_path = data_path / 'img' / f'{chat_id}{str(datetime.now()).replace(":", "_").replace(".", "_")}.png'
        msg_qty_data = db.view_msg_qty_for_channel(chat_id, channel_name)

        if msg_qty_data:
            save_datetime_graph("Анализ количества сообщений", VIEW_MSG_QTY,
                                file_path, msg_qty_data, channel_name)
            await bot.send_photo(chat_id, types.InputFile(str(file_path)),
                                 f' График количества сообщений для канала {channel_name}')
        else:
            await bot.send_message(chat_id,
                                   f'Нет данных по количеству сообщений для канала {channel_name}')
    except DbExceptions.TgChatIsNotSubscribedToTwChannel:
        await bot.send_message(chat_id, f'Вы уже не подписаны на канал {channel_name}')
