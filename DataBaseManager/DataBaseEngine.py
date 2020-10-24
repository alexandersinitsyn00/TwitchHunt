import sqlite3
from datetime import datetime


class DataBaseEngine:
    def __init__(self, database_path: str):
        self.db = sqlite3.connect(database_path)
        self.cursor = self.db.cursor()
        self.__create_schema__()

    def __create_schema__(self):
        # Канал
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS twitch_channel 
                          ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT unique
                          )
                       """)

        # Пользователь
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS twitch_user 
                          ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT unique
                          )
                       """)

        # Чат
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

    def save_twitch_message(self, channel: str, user: str, msg: str):
        self.cursor.execute('INSERT or IGNORE INTO twitch_channel (name) VALUES (?)', (channel,))
        self.cursor.execute('INSERT or IGNORE INTO twitch_user (name) VALUES (?)', (user,))
        self.cursor.execute("""INSERT INTO twitch_chat (channel_id, user_id, msg, unix_datetime) 
                                    SELECT c.id, u.id, ?, ?
                                    FROM twitch_user u
                                        JOIN twitch_channel c on c.name = ?
                                    WHERE u.name = ?
                           """, (msg, datetime.now().timestamp(), channel, user))
        self.db.commit()

    def get_all_channels(self):
        return self.cursor.execute('SELECT * FROM twitch_channel')