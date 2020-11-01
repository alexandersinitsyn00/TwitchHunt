from os import environ
from aiogram import types
from aiogram.utils.markdown import text, bold
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode

from DataBase import *

from ..telegram import dp
from ..keyboards_stickers import *

from .. import states

root_path = environ.get("ROOT_DIR")
data_folder = environ.get("DATA_DIR")


# START COMMAND
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    chat_id = message.chat.id
    user = message.from_user

    db.add_tg_chat(chat_id, user.first_name, user.last_name,
                   user.username, user.language_code)

    await message.answer_sticker(HELLO_DOG_STICKER)
    await message.answer("""Привет! Это бот для аналитики каналов Twitch! 😇
        Чтобы получить подробный список возможностей
        вы можете воспользоваться командой /help
        или нажать кнопку на клавиатуре
    """, reply_markup=start_keyboard)


# HELP COMMAND
@dp.message_handler(commands=['help'])
@dp.message_handler(text=show_info_button.text)
async def process_start_command(message: types.Message):
    await message.answer_sticker(HMM_DOG_STICKER)
    await message.answer("""Бот позволяет следить за каналами TWITCH
    Для начала необходимо подписаться на канал. /sub        
        Нужно будет ввести имя канала, на который вы хотите подписаться
    После создания подписки начинается отслеживание чата, количества зрителей и другой информации
    Так же при желании от канала можно отписаться. /unsub        

    Для получения информации о канале необоходимо открыть список подписок /mysubs и выбрать канал, тип получаемых данных

    """, reply_markup=start_keyboard)


# SUBSCRIBE COMMAND
@dp.message_handler(commands=['sub'])
@dp.message_handler(text=subscribe_button.text)
async def process_subscribe_command(message: types.Message):
    db.set_state_for_tg_chat(message.chat.id, states.SUBSCRIBING)

    resp_text = text('Пожалуйста, введите',
                     bold('имя канала'),
                     'на который вы хотите подписаться'
                     )
    await message.answer(resp_text, parse_mode=ParseMode.MARKDOWN)


# UNSUBSCRIBE COMMAND
@dp.message_handler(commands=['unsub'])
@dp.message_handler(text=unsubscribe_button.text)
async def process_unsubscribe_command(message: types.Message):
    db.set_state_for_tg_chat(message.chat.id, states.UNSUBSCRIBING)
    resp_text = text('Пожалуйста, введите',
                     bold('имя канала'),
                     'от которого вы хотите отписаться'
                     )
    await message.answer(resp_text, parse_mode=ParseMode.MARKDOWN)


# MYSUB COMMAND
@dp.message_handler(commands=['mysubs'])
@dp.message_handler(text=my_subs_button.text)
async def process_mysub_list_command(message: types.Message):
    channels_data = db.get_subscribed_channels(message.chat.id)
    if not channels_data:
        await message.answer('Вы не были подписаны ни на один канал')
        return

    subs_keyboard = InlineKeyboardMarkup(row_width=4)
    for row in channels_data:
        channel_name = row[0]
        btn = InlineKeyboardButton(channel_name, callback_data=f'channel:{channel_name}')
        subs_keyboard.insert(btn)

    await message.answer('Выберите канал для взаимодействия', reply_markup=subs_keyboard)
