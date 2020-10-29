from aiogram import types
from Telegram.misc import dp
from DataBaseManager.misc import db
from GraphBuilder.GraphBuilder import multiply_datetime_graph

from Telegram import states


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    chat = message['chat']
    user_from = message['from']
    db.save_telegram_user_info(chat['id'],
                               user_from['first_name'],
                               user_from['last_name'],
                               user_from['username'],
                               user_from['language_code'])
    await message.answer("Привет! Это бот для анализа Twitch!")


@dp.message_handler(commands=['sub'])
async def cmd_start(message: types.Message):
    chat_id = message['chat']['id']
    db.set_state_for_telegram_user(chat_id, states.SUBSCRIBING)
    await message.answer('Введите имя канала, на которой вы хотите подписаться: ')


@dp.message_handler(commands=['unsub'])
async def cmd_start(message: types.Message):
    chat_id = message['chat']['id']
    db.set_state_for_telegram_user(chat_id, states.UNSUBSCRIBING)
    await message.answer('Введите имя канала, от которого вы хотите отписаться')


@dp.message_handler(commands=['msg_qty'])
async def cmd_start(message: types.Message):
    chat_id = message['chat']['id']
    db.set_state_for_telegram_user(chat_id, states.WANTING_GRAPH)
    await message.answer('Введите имя канала, для которого вы хотите получить график с количеством сообщений: ')


@dp.message_handler(commands=['mysubs'])
async def cmd_start(message: types.Message):
    chat_id = message['chat']['id']
    channels = db.get_list_of_channels_per_telegram_chat(chat_id)
    msg = ''
    for row in channels:
        msg = f'{msg}\n{row[0]}'
    await message.answer(f'Список ваших подписок: {msg}')


@dp.message_handler(commands=['all_msg_qty'])
async def cmd_start(message: types.Message):
    chat_id = message['chat']['id']
    channels = db.get_list_of_channels_per_telegram_chat(chat_id)

    graph_data = {}
    graph_name = 'Анализ количества сообщений'
    count = 0
    for row in channels:
        count = count + 1
        channel_name = row[0]
        graph_data[channel_name] = db.VIEW_MESSAGES_COUNT_PER_MINUTE_FOR_CHANNEL(channel_name)

    if count > 0:
        multiply_datetime_graph(graph_name, 'Количество сообщений', chat_id, graph_data)
        await message.answer_photo(types.InputFile(f'C:/Users/Warzik/Desktop/Test/TwitchHunt/Data/{chat_id}.jpg'),
                               f'{graph_name} для всех подписок')
    else:
        message.answer("Вы не подписаны ни ни один канал")
