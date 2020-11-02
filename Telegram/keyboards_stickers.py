from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

HELLO_DOG_STICKER = 'CAACAgIAAxkBAAIZHV-ciw8XV9KmxBzp-qiJq6eHh_FVAALTAANWnb0K9TKPl9US-T0bBA'
HMM_DOG_STICKER = 'CAACAgIAAxkBAAIa1F-dW83mNAhFuXVwQPAQYQQraB5nAALjAANWnb0KD_gizK2mCzcbBA'

show_info_button = KeyboardButton("Помощь❔")
subscribe_button = KeyboardButton("Подписаться на канал Twitch 📌")
my_subs_button = KeyboardButton("Список моих подписок 📃")

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
start_keyboard.row(subscribe_button). \
    row(my_subs_button). \
    insert(show_info_button)
