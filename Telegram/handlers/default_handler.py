from aiogram import types
from Telegram.misc import dp
from DataBaseManager.misc import db
from Telegram import states


@dp.message_handler()
async def echo(message: types.Message):
    chat_id = message['chat']['id']
    state = db.get_state_for_telegram_user(chat_id)
    print(state)
    if state == states.DOING_NOTHING:
        await message.answer('Пожалуйста, выберите команду')
    elif state == states.SUBSCRIBING:
        await message.answer('Вы ввели имя канала, на который хотите подписаться')
        db.update_state_for_telegram_user(chat_id, 0)
