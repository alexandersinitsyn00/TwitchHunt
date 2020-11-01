import sqlite3
from .Exceptions import *


def get_listening_channels(self):
    stream_id = self.cursor.execute("""
                                    SELECT tw_channel.name
                                    FROM tw_channel
                                    WHERE tw_channel.IS_LISTENING_STATE = 1
                                """, ).fetchall()
    return stream_id


def get_tw_channel_id_by_name(self, channel_name: str):
    try:
        channel_name = channel_name.lower()
        channel_id = self.cursor.execute("""
                                    SELECT ID FROM tw_channel
                                    WHERE name = ?
                                    LIMIT 1
                                """, (channel_name,)).fetchone()[0]
    except IndexError:
        raise TwChannelNotFound
    return channel_id


def get_tw_user_id_by_name(self, user_name):
    try:
        user_id = self.cursor.execute("""
                                    SELECT ID FROM tw_user
                                    WHERE name = ?
                                    LIMIT 1
                                """, (user_name,)).fetchone()[0]
    except IndexError:
        raise TwUserNotFound
    return user_id


def get_active_stream_id_for_channel(self, channel_id: str):
    try:
        stream_id = self.cursor.execute("""
                                    SELECT tw_stream.ID 
                                    FROM tw_stream 
                                        JOIN tw_channel on tw_channel.id = tw_stream.channel_id
                                    WHERE tw_channel.id = ?
                                    ORDER BY tw_stream.ID DESC
                                    LIMIT 1
                                """, (channel_id,)).fetchone()[0]
    except (IndexError, TypeError):
        raise TwStreamNotFound
    return stream_id


def get_state_for_tg_chat(self, chat_id):
    try:
        state = self.cursor.execute("""
                                        SELECT STATE 
                                        FROM  tg_chat
                                        WHERE id = ?
                                        LIMIT 1
                                """, (chat_id,)).fetchone()[0]
    except IndexError:
        raise TgChatNotFound
    return state


def get_tasks_from_channel_actions_deque(self):
    return self.cursor.execute("""
                            SELECT *
                            FROM tw_channel_actions_deque
                        """).fetchall()


def is_tg_chat_has_sub_to_tw_channel(self, chat_id, channel_id):
    res = self.cursor.execute("""
                            SELECT ref_tg_tw.id
                            FROM ref_tg_tw 
                                JOIN tg_chat on tg_chat.id = ref_tg_tw.tg_chat_id
                                JOIN tw_channel on tw_channel.id = ref_tg_tw.tw_channel_id
                            WHERE tg_chat.id = ? AND tw_channel.id = ?
                            LIMIT 1
                        """, (chat_id, channel_id)).fetchone()
    if res:
        return True


def is_stream_added(self, stream_id):
    res = self.cursor.execute("""
                            SELECT ID FROM tw_stream where ID = 
                        """, (stream_id,)).fetchone()
    if res:
        return True
