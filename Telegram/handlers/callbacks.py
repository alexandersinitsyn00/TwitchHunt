from os import environ
from pathlib import Path
from datetime import datetime as dt
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

actions = [
    VIEW_MSG_QTY]


# channel callback
@dp.callback_query_handler(lambda query: query.data.startswith('channel:'))
async def process_channel_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    channel = callback_query.data.replace('channel:', '')
    act_keyboard = InlineKeyboardMarkup(row_width=2)
    for act in actions:
        btn = InlineKeyboardButton(act, callback_data=f'act:{act}_channel:{channel}')
        act_keyboard.insert(btn)
    await bot.send_message(callback_query.from_user.id,
                           f'Выберите опцию для канала {channel}',
                           reply_markup=act_keyboard)


# action for channel callback
@dp.callback_query_handler(lambda query: query.data.startswith('act:'))
async def process_action_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    chat_id = callback_query.message.chat.id

    data = callback_query.data.replace('act:', '').replace('channel:', '').split('_')
    act = data[0]
    channel = data[1]
    try:
        if act == VIEW_MSG_QTY:
            file_path = data_path / 'img' / f'{chat_id}{str(datetime.now()).replace(":", "_").replace(".", "_")}.png'
            msg_qty_data = db.view_msg_qty_for_channel(chat_id, channel)
            if msg_qty_data:
                save_datetime_graph("Анализ количества сообщений", VIEW_MSG_QTY,
                                    file_path, msg_qty_data, channel)
                await bot.send_photo(chat_id, types.InputFile(str(file_path)),
                                     f' График количества сообщений для канала {channel}')
            else:
                await bot.send_message(callback_query.from_user.id,
                                       f'Нет данных по количеству сообщений для канала {channel}')

    except DbExceptions.TgChatIsNotSubscribedToTwChannel:
        await bot.send_message(callback_query.from_user.id, f'Вы уже не подписаны на канал {channel}')
        return

    # await bot.send_message(callback_query.from_user.id, f'НЕ РЕАЛИЗОВАНО. {act} {channel}')
