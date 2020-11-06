import sqlite3
from datetime import datetime
from .Exceptions import *
import pytz


def add_tw_stream(self, data):
    stream_id = data["stream_id"]
    channel_name = data["channel_name"]
    datetime_create = data["datetime_create"]

    channel_id = self.get_tw_channel_id_by_name(channel_name)

    self.cursor.execute("""INSERT or IGNORE INTO tw_stream (ID, channel_id, datetime_begin)
                            VALUES (?, ?, ?)
                        """, (stream_id, channel_id, datetime_create))
    self.db.commit()


def add_tw_stream_info(self, data):
    stream_id = data["stream_id"]
    viewers_count = data["viewer_count"]

    utc_date_time = pytz.utc.localize(datetime.utcnow())
    moscow_timezone = pytz.timezone('Europe/Moscow')
    moscow_date_time_now = utc_date_time.astimezone(moscow_timezone)

    self.cursor.execute("""INSERT or IGNORE INTO tw_stream_history (stream_id, viewers_count, datetime_create)
                            VALUES (?, ?, ?)
                        """, (stream_id, viewers_count, str(moscow_date_time_now)))
    self.db.commit()


def add_tw_subscription(self, tg_chat_id: str, channel_name: str):
    self.add_tw_channel(channel_name)

    channel_id = self.get_tw_channel_id_by_name(channel_name)
    try:
        self.cursor.execute("""INSERT INTO ref_tg_tw (tw_channel_id, tg_chat_id)
                                VALUES(?, ?)
                            """, (channel_id, tg_chat_id))
        self.db.commit()
    except sqlite3.IntegrityError:
        raise TgChatAlreadySubscribedToTwChannel


def add_tw_channel(self, tw_channel_name: str):
    self.cursor.execute("""
                        INSERT or IGNORE INTO tw_channel (name, IS_LISTENING_STATE)
                            VALUES (?, 1) 
                        """, (tw_channel_name,))
    self.db.commit()


def add_tw_user(self, tw_user_name: str):
    self.cursor.execute("""
                        INSERT or IGNORE INTO tw_user (name)
                            VALUES (?) 
                        """, (tw_user_name,))
    self.db.commit()


def add_tg_chat(self, chat_id: str, first_name: str,
                last_name: str, user_name: str,
                language_code: str):
    self.cursor.execute("""
                        INSERT or IGNORE INTO tg_chat (ID, first_name, last_name,
                                            user_name, language_code,
                                            STATE)
                            VALUES (?, ?, ?, ?, ?, 0) 
                        """, (chat_id, first_name, last_name,
                              user_name, language_code))
    self.db.commit()


def add_twitch_message(self, channel_name: str, tw_user_name: str, msg: str):
    channel_id = self.get_tw_channel_id_by_name(channel_name)
    self.add_tw_user(tw_user_name)

    stream_id = self.get_active_stream_id_for_channel(channel_id)
    user_id = self.get_tw_user_id_by_name(tw_user_name)

    utc_date_time = pytz.utc.localize(datetime.utcnow())
    moscow_timezone = pytz.timezone('Europe/Moscow')
    moscow_date_time_now = utc_date_time.astimezone(moscow_timezone)

    self.cursor.execute("""INSERT INTO tw_chat (stream_id, user_id, msg, datetime_create)
                                VALUES (?, ?, ?, ?)
                       """, (stream_id, user_id, msg, str(moscow_date_time_now)))


def __add_tasks_by_init__(self):
    self.cursor.execute("""
                        INSERT INTO tw_channel_actions_deque (action, tw_channel_name)
                        SELECT 'JOIN', tw_channel.name
                        FROM tw_channel
                        """)
    self.db.commit()
