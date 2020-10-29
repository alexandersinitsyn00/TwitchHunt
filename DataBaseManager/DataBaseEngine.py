import sqlite3
from datetime import datetime
from DataBaseManager.Exceptions import TelegramChatHasNoSubToChannel


class DataBaseEngine:
    def __init__(self):
        self.db = None
        self.cursor = None

    def setup(self, database_path: str):
        self.db = sqlite3.connect(database_path)
        self.cursor = self.db.cursor()
        self.__create_schema__()

    # Создание подписки
    def add_subscription(self, chat_id, channel_name):
        self.__add_twitch_channel_if_not_exists__(channel_name)
        self.cursor.execute("""INSERT INTO ref_telegram_twitch (telegram_id, channel_id) 
                                    SELECT telegram.id, channel.id
                                    FROM telegram
                                        JOIN twitch_channel channel on channel.name = ?
                                    WHERE telegram.chat_id = ?
                            """, (channel_name, chat_id))
        self.db.commit()

    # Удаление подписки
    def remove_subscription(self, chat_id, channel_name):
        if not self.is_telegram_chat_has_sub_to_channel(chat_id, channel_name):
            raise TelegramChatHasNoSubToChannel()
        self.cursor.execute("""
                           DELETE FROM ref_telegram_twitch 
                                WHERE telegram_id = (select id from telegram
                                                    where chat_id = ?)
                                AND channel_id = (select ID from twitch_channel
                                                    where name = ?) 
                            """, (chat_id, channel_name))
        self.db.commit()

    # Сохранение сообщения
    def save_twitch_message(self, channel: str, user: str, msg: str):
        self.__add_twitch_channel_if_not_exists__(channel)
        self.__add_twitch_user_if_not_exists__(user)
        self.cursor.execute("""INSERT INTO twitch_chat (channel_id, user_id, msg, date, time) 
                                    SELECT c.id, u.id, ?, ?, ?
                                    FROM twitch_user u
                                        JOIN twitch_channel c on c.name = ?
                                    WHERE u.name = ?
                           """, (
            msg, datetime.now().date(), str(datetime.now().time()), channel, user))
        self.db.commit()

    # Сохранение информации о пользователе Telegram
    def save_telegram_user_info(self, chat_id, first_name, last_name, user_name, language_code):
        self.cursor.execute("""INSERT or IGNORE INTO telegram
                                    (chat_id, first_name, last_name, user_name, language_code, STATE) 
                               VALUES (?, ?, ?, ?, ?, ?) 
                            """, (chat_id, first_name, last_name, user_name, language_code, '0'))
        self.db.commit()

    # Установка состояния для канала Твича
    def set_state_for_twitch_channel(self, channel_name, state):
        self.cursor.execute("""UPDATE twitch_channel
                                    SET IS_LISTENING_STATE = ?
                                    WHERE name = ?
        """, (state, channel_name))
        self.db.commit()

    # Установка состояния для пользователя Телеграмма
    def set_state_for_telegram_user(self, chat_id, state: int):
        self.cursor.execute("""UPDATE telegram
                                    SET STATE = ?
                                    WHERE chat_id = ?
        """, (state, chat_id))
        self.db.commit()

    # Получение состояния для пользователя телеграмм
    def get_state_for_telegram_user(self, chat_id):
        res = self.cursor.execute("""SELECT STATE FROM telegram WHERE chat_id = ?
            """, (chat_id,))
        for row in res:
            if row is not None:
                return row[0]

    # Проверка, подписаны ли на канал пользователи Telegram
    def is_channel_has_subscriptions(self, channel_name):
        query_res = self.cursor.execute("""
            select subs.id 
            from twitch_channel channel
                join ref_telegram_twitch subs on subs.channel_id = channel.id
            where channel.name = ?
        """, (channel_name,))
        for row in query_res:
            if row is not None:
                return True
        return False

    # Получение списка каналов Twitch, которые нужно прослушивать
    def get_list_of_listening_channels(self):
        res = self.cursor.execute("""SELECT name from twitch_channel WHERE IS_LISTENING_STATE = 1""")
        channels_list = []
        for row in res:
            channels_list.append(row[0])
        return channels_list

    # Получение количества сообщений для канала поминутно
    def VIEW_MESSAGES_COUNT_PER_MINUTE_FOR_CHANNEL(self, channel_name):
        return self.cursor.execute("""
                    SELECT COUNT(*), tw_chat.date, SUBSTR(tw_chat.time, 1,5)
                    FROM twitch_chat tw_chat
                        JOIN twitch_channel channel on tw_chat.channel_id = channel.id
                    WHERE channel.name = ?
                    GROUP by tw_chat.date, SUBSTR(tw_chat.time, 1,5)
                    """, (channel_name,))

    # Получение количества зрителей для канала поминутно
    def VIEW_VIEWERS_COUNT_PER_MINUTE_FOR_CHANNEL(self, channel_name):
        return self.cursor.execute("""
                    SELECT MAX(viewers), date, SUBSTR(time, 1,5)
                    FROM twitch_streams_info
                        JOIN twitch_channel channel on twitch_streams_info.channel_id = channel.id
                    WHERE channel.name = ?
                    GROUP by date, SUBSTR(time, 1,5)
                    """, (channel_name,))

    # Добавить канал в базу, если его не существует
    def __add_twitch_channel_if_not_exists__(self, channel_name):
        self.cursor.execute('INSERT or IGNORE INTO twitch_channel (name, IS_LISTENING_STATE) VALUES (?, 1)',
                            (channel_name,))
        self.db.commit()

    # Добавить пользователя в базу, если его еще не существует
    def __add_twitch_user_if_not_exists__(self, user_name):
        self.cursor.execute('INSERT or IGNORE INTO twitch_user (name) VALUES (?)', (user_name,))
        self.db.commit()

    # Добавить информацию о стриме
    def save_stream_info(self, channel_name, game_id, language, title, viewers):
        self.cursor.execute("""INSERT  INTO twitch_streams_info (game_id, language, title, 
                                                                viewers,  date, time, channel_id)
                                    SELECT ?, ?, ?, ? , ?, ?, id
                                    FROM twitch_channel
                                    WHERE name = ? 
                            """,
                            (game_id, language, title, viewers, datetime.now().date(), str(datetime.now().time()),
                             channel_name))
        self.db.commit()

        # Проверка, имеет ли пользователь телеграмма подписку на канал

    def is_telegram_chat_has_sub_to_channel(self, chat_id, channel_name):
        query_res = self.cursor.execute("""
            select ref.id 
            from ref_telegram_twitch ref
                join telegram on ref.telegram_id = telegram.id and telegram.chat_id = ?
                join twitch_channel channel on ref.channel_id = channel.id and channel.name = ?
        """, (chat_id, channel_name))
        for row in query_res:
            if row is not None:
                return True
        return False

    # Создание схемы БД
    def __create_schema__(self):
        # Канал твича
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS twitch_channel 
                          ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT unique,
                            IS_LISTENING_STATE INTEGER
                          )
                       """)

        # Информация о стримах канала
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS twitch_streams_info
                           ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
                              game_id INTEGER,
                              language,
                              title,
                              viewers,
                              channel_id INTEGER,
                              date TEXT,
                              time TEXT,
                              FOREIGN KEY(channel_id) REFERENCES twitch_channel(ID)
                           )
                        """)

        # Пользователь твича
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS twitch_user 
                          ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT unique
                          )
                       """)

        # Чат твича
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS twitch_chat
                          ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            channel_id INTEGER,
                            user_id INTEGER,
                            msg TEXT,
                            date TEXT,
                            time TEXT,
                            FOREIGN KEY(channel_id) REFERENCES twitch_channel(ID),
                            FOREIGN KEY(user_id) REFERENCES twitch_user(ID)
                          )
                       """)

        # Пользователь телеграмма
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS telegram
                          ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            chat_id INTEGER unique,
                            first_name unique,
                            last_name TEXT,
                            user_name TEXT,
                            language_code TEXT,
                            STATE INTEGER
                          )
                       """)

        # Связь пользователь телеграмма - канал TWITCH
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS ref_telegram_twitch 
                          ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            telegram_id INTEGER,
                            channel_id INTEGER,
                            FOREIGN KEY(channel_id) REFERENCES twitch_channel(ID),
                            FOREIGN KEY(telegram_id) REFERENCES telegram(ID)
                            UNIQUE(telegram_id, channel_id)
                          )
                       """)
