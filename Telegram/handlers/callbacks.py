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
VIEW_MOST_ACTIVE_USERS = 'ТОП зрителей'
UNSUB = 'Отписаться'
VIEW_STREAMS = 'Информация по дням'

actions = [
    UNSUB,
    VIEW_STREAMS,
    VIEW_MSG_QTY,
    VIEW_VIWERS_COUNT_QTY,
    VIEW_MOST_ACTIVE_USERS
]

NON_STREAMS_ACTIONS = 2


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


@dp.callback_query_handler(lambda query: query.data.startswith('date:'))
async def process_action_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    data = callback_query.data.replace('date:', '').replace('channel:', '').split('*')

    date = data[0]
    channel = data[1]

    act_keyboard = InlineKeyboardMarkup(row_width=2)
    for act in actions[NON_STREAMS_ACTIONS:]:
        btn = InlineKeyboardButton(act, callback_data=f'da:{act}*ch:{channel}*dt:{date}')
        act_keyboard.insert(btn)
    await bot.send_message(callback_query.from_user.id,
                           f'Выберите опцию. Канал: {channel}. Дата трансляции: {date}',
                           reply_markup=act_keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith('act:'))
async def process_action_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    chat_id = callback_query.message.chat.id

    data = callback_query.data.replace('act:', '').replace('channel:', '').split('*')
    act = data[0]
    channel = data[1]
    if act == VIEW_MSG_QTY:
        await create_send_qty_msg_graph(chat_id, channel)

    elif act == VIEW_VIWERS_COUNT_QTY:
        await create_send_viewers_msg_graph(chat_id, channel)

    elif act == UNSUB:
        await unsubscribing(chat_id, channel)

    elif act == VIEW_STREAMS:
        user_from = callback_query.from_user.id
        await show_streams(chat_id, channel, user_from)

    elif act == VIEW_MOST_ACTIVE_USERS:
        await send_most_active_users(chat_id, channel)


@dp.callback_query_handler(lambda query: query.data.startswith('da:'))
async def process_action_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    chat_id = callback_query.message.chat.id

    data = callback_query.data.replace('da:', '').replace('ch:', '').replace('dt:', '').split('*')
    act = data[0]
    channel = data[1]
    date = data[2]

    if act == VIEW_MSG_QTY:
        await create_send_qty_msg_graph(chat_id, channel, date=date)
    elif act == VIEW_VIWERS_COUNT_QTY:
        await create_send_viewers_msg_graph(chat_id, channel, date=date)
    elif act == VIEW_MOST_ACTIVE_USERS:
        await send_most_active_users(chat_id, channel, date)


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


async def create_send_qty_msg_graph(chat_id, channel_name, date=None):
    try:
        file_path = data_path / 'img' / f'{chat_id}{str(datetime.now()).replace(":", "_").replace(".", "_")}.png'
        msg_qty_data = db.view_msg_qty_for_channel(chat_id, channel_name, date)

        if msg_qty_data:
            await create_send_graph('График количества сообщений',
                                    'Анализ количества сообщений',
                                    'Количество сообщений',
                                    file_path,
                                    msg_qty_data,
                                    channel_name,
                                    chat_id)
        else:
            await bot.send_message(chat_id,
                                   f'Нет данных по количеству сообщений')
    except DbExceptions.TgChatIsNotSubscribedToTwChannel:
        await bot.send_message(chat_id, f'Вы уже не подписаны на канал {channel_name}')


async def send_most_active_users(chat_id, channel_name, date=None):
    try:
        most_active_users = db.view_most_active_user_for_channel(chat_id, channel_name, date)

        if most_active_users:
            msg = f'Наиболее активные пользователи на канале {channel_name}🥰 за {"все время" if not date else date} :\n'
            counter = 1
            for row in most_active_users:
                msg = msg + f'{counter:^4}: {row[0]:<30} {row[1]:>5} сообщений\n'
                counter = counter + 1
            await bot.send_message(chat_id, msg)
        else:
            await bot.send_message(chat_id, f'На канале {channel_name} еще нет сообщений')
    except DbExceptions.TgChatIsNotSubscribedToTwChannel:
        await bot.send_message(chat_id, f'Вы уже не подписаны на канал {channel_name}')


async def create_send_viewers_msg_graph(chat_id, channel_name, date=None):
    try:
        file_path = data_path / 'img' / f'{chat_id}{str(datetime.now()).replace(":", "_").replace(".", "_")}.png'
        viewers_count_data = db.view_viewers_qty_for_channel(chat_id, channel_name, date)

        if viewers_count_data:
            await create_send_graph('График количества зрителей',
                                    'Анализ количества зрителей',
                                    'Количество зрителей',
                                    file_path,
                                    viewers_count_data,
                                    channel_name,
                                    chat_id)
        else:
            await bot.send_message(chat_id,
                                   f'Нет данных по количеству зрителей')
    except DbExceptions.TgChatIsNotSubscribedToTwChannel:
        await bot.send_message(chat_id, f'Вы уже не подписаны на канал {channel_name}')


async def create_send_graph(msg, graph_name, y_label, file_path, data, channel_name, chat_id):
    save_datetime_graph(graph_name, y_label,
                        file_path, data, channel_name)
    await bot.send_photo(chat_id, types.InputFile(str(file_path)),
                         f' {msg} {channel_name}')


async def show_streams(chat_id, channel, user_from):
    try:
        streams_keyboard = InlineKeyboardMarkup(row_width=4)
        for row in db.get_channell_stream_dates(chat_id, channel):
            btn = InlineKeyboardButton(row[0], callback_data=f'date:{row[0]}*channel:{channel}')
            streams_keyboard.insert(btn)
        await bot.send_message(user_from,
                               f'Выберите дату для получения информации по каналу {channel}',
                               reply_markup=streams_keyboard)
    except DbExceptions.TgChatIsNotSubscribedToTwChannel:
        await bot.send_message(user_from,
                               f'Вы уже не подписаны на канал {channel}')
