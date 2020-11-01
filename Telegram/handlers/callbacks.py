from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..telegram import dp
from ..telegram import bot


# channel callback
@dp.callback_query_handler(lambda query: query.data.startswith('channel:'))
async def process_channel_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    actions = ['Кол-во сообщений',
               'Кол-во зрителей']
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

    data = callback_query.data.replace('act:', '').replace('channel:', '').split('_')
    act = data[0]
    channel = data[1]
    await bot.send_message(callback_query.from_user.id, f'НЕ РЕАЛИЗОВАНО. {act} {channel}')
