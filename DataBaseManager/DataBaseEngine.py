import sqlite3
from datetime import datetime


class DataBaseEngine:
    def __init__(self):
        self.db = None
        self.cursor = None

    def setup(self, database_path: str):
        self.db = sqlite3.connect(database_path)
        self.cursor = self.db.cursor()
        self.__create_schema__()

    def __create_schema__(self):
        # Канал твича
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS twitch_channel 
                          ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT unique,
                            IS_LISTENING_STATE INTEGER
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
                            unix_datetime REAL,
                            FOREIGN KEY(channel_id) REFERENCES twitch_channel(ID),
                            FOREIGN KEY(user_id) REFERENCES twitch_user(ID)
                          )
                       """)

        # Пользователь телеграмма
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS telegram_chat
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
                            chat_id INTEGER,
                            channel_id INTEGER,
                            FOREIGN KEY(channel_id) REFERENCES twitch_channel(ID),
                            FOREIGN KEY(chat_id) REFERENCES telegram_chat(ID)
                            UNIQUE(chat_id, channel_id)
                          )
                       """)

    def add_subscription(self, chat_id, channel_name):
        self.__add_twitch_channel_if_not_exists__(channel_name)
        self.cursor.execute("""INSERT INTO ref_telegram_twitch (chat_id, channel_id) 
                                    SELECT chat.id, channel.id
                                    FROM telegram_chat chat 
                                        JOIN twitch_channel channel on channel.name = ?
                                    WHERE chat.chat_id = ?
                            """, (channel_name, chat_id))

    def remove_subscription(self, chat_id, channel_name):
        self.cursor.execute("""
                           DELETE FROM ref_telegram_twitch 
                                WHERE chat_id = (select id from telegram_chat
                                                    where chat_id = ?)
                                AND channel_id = (select ID from twitch_channel
                                                    where name = ?) 
                            """, (chat_id, channel_name))

    def save_twitch_message(self, channel: str, user: str, msg: str):
        self.__add_twitch_channel_if_not_exists__(channel)
        self.__add_twitch_user_if_not_exists__(user)
        self.cursor.execute("""INSERT INTO twitch_chat (channel_id, user_id, msg, unix_datetime) 
                                    SELECT c.id, u.id, ?, ?
                                    FROM twitch_user u
                                        JOIN twitch_channel c on c.name = ?
                                    WHERE u.name = ?
                           """, (msg, datetime.now().timestamp(), channel, user))
        self.db.commit()

    def save_telegram_user_info(self, chat_id, first_name, last_name, user_name, language_code):
        self.cursor.execute("""INSERT or IGNORE INTO telegram_chat 
                                    (chat_id, first_name, last_name, user_name, language_code, STATE) 
                               VALUES (?, ?, ?, ?, ?, ?) 
                            """, (chat_id, first_name, last_name, user_name, language_code, '0'))
        self.db.commit()

    def set_state_for_telegram_user(self, chat_id, state: int):
        self.cursor.execute("""UPDATE telegram_chat
                                    SET STATE = ?
                                    WHERE chat_id = ?
        """, (state, chat_id))
        self.db.commit()

    def get_state_for_telegram_user(self, chat_id):
        res = self.cursor.execute("""SELECT STATE FROM telegram_chat WHERE chat_id = ?
            """, (chat_id,))
        for row in res:
            if row is not None:
                return row[0]

    def __add_twitch_channel_if_not_exists__(self, channel_name):
        self.cursor.execute('INSERT or IGNORE INTO twitch_channel (name, IS_LISTENING_STATE) VALUES (?, 1)',
                            (channel_name,))
        self.db.commit()

    def __add_twitch_user_if_not_exists__(self, user_name):
        self.cursor.execute('INSERT or IGNORE INTO twitch_user (name) VALUES (?)', (user_name,))
        self.db.commit()

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
