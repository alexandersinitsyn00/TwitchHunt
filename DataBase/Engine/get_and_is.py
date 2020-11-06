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


def get_subscribed_channels(self, chat_id):
    res = self.cursor.execute("""
                            SELECT tw_channel.name
                            FROM ref_tg_tw 
                                JOIN tg_chat on tg_chat.id = ref_tg_tw.tg_chat_id
                                JOIN tw_channel on tw_channel.id = ref_tg_tw.tw_channel_id
                            WHERE tg_chat.id = ?
                        """, (chat_id,)).fetchall()
    if res:
        return res


def view_msg_qty_for_channel(self, chat_id, channel_name):
    channel_id = self.get_tw_channel_id_by_name(channel_name)

    if not self.is_tg_chat_has_sub_to_tw_channel(chat_id, channel_id):
        raise TgChatIsNotSubscribedToTwChannel

    res = self.cursor.execute("""
                    SELECT COUNT(*), substr(tw_chat.datetime_create, 1, 16)
                    FROM tw_chat
	                    INNER JOIN tw_stream on tw_chat.stream_id = tw_stream.id
	                    INNER JOIN tw_channel on tw_stream.channel_id= tw_channel.id
	                WHERE tw_channel.id = ?
                    GROUP BY tw_channel.ID, substr(tw_chat.datetime_create, 1, 16)
                    """, (channel_id,)).fetchall()
    if res:
        return res


def view_viewers_qty_for_channel(self, chat_id, channel_name):
    channel_id = self.get_tw_channel_id_by_name(channel_name)

    if not self.is_tg_chat_has_sub_to_tw_channel(chat_id, channel_id):
        raise TgChatIsNotSubscribedToTwChannel

    res = self.cursor.execute("""
                    SELECT tw_stream_history.viewers_count, substr(tw_stream_history.datetime_create, 1, 16)
                    FROM tw_stream_history
	                    INNER JOIN tw_stream on tw_stream_history.stream_id = tw_stream.id
	                    INNER JOIN tw_channel on tw_stream.channel_id= tw_channel.id
	                WHERE tw_channel.id = ?
                    GROUP BY tw_channel.ID, substr(tw_stream_history.datetime_create, 1, 16)
                    """, (channel_id,)).fetchall()
    if res:
        return res


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
