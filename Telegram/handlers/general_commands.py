from aiogram import types
from Telegram.misc import dp
from DataBaseManager.misc import db
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
    db.update_state_for_telegram_user(chat_id, states.SUBSCRIBING)
    await message.answer('Введите имя канала, на которой вы хотите подписаться: ')
