import sqlite3
from datetime import datetime


class DataBaseEngine:
    def __init__(self, database_path: str):
        self.db = sqlite3.connect(database_path)
        self.cursor = self.db.cursor()
        self.__create_schema__()

    def __create_schema__(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS twitch_chat
                          (channel, user, msg, unix_datetime)
                       """)

    def print_chat_history(self):
        for row in self.cursor.execute("SELECT * FROM twitch_chat"):
            print(row)

    def print_most_active_users_for_channel(self, channel, limit=10):
        for row in self.cursor.execute(f"SELECT user, COUNT(*) FROM twitch_chat WHERE channel = '{channel}'"
                                       f"GROUP BY channel, user ORDER BY COUNT(*) DESC LIMIT {limit}"):
            print(row)

    def save_twitch_message(self, channel, user, msg):
        self.cursor.execute(f"""INSERT INTO twitch_chat (channel, user, msg, unix_datetime)
                                VALUES ('{channel}', '{user}', '{msg}', {datetime.now().timestamp()})""")
        self.db.commit()
