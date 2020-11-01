import sqlite3
from datetime import datetime
from .Exceptions import *


def remove_tw_subscription(self, tg_chat_id: str, channel_name: str):
    try:
        channel_id = self.get_tw_channel_id_by_name(channel_name)
    except TypeError:
        raise TgChatIsNotSubscribedToTwChannel

    if not self.is_tg_chat_has_sub_to_tw_channel(tg_chat_id, channel_id):
        raise TgChatIsNotSubscribedToTwChannel
    self.cursor.execute("""DELETE FROM ref_tg_tw
                                WHERE tg_chat_id = ? AND tw_channel_id =?
                            """, (tg_chat_id, channel_id))
    self.db.commit()


def remove_task_from_channel_actions_deque(self, task_id):
    self.cursor.execute("""DELETE FROM tw_channel_actions_deque
                                WHERE ID = ? 
                            """, (task_id,))
    self.db.commit()
