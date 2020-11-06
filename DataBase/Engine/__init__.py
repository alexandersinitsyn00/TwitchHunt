import sqlite3


class DbEngine(object):
    def __init__(self, db_file_path: str):
        self.db = sqlite3.connect(db_file_path)
        self.cursor = self.db.cursor()
        self.__create_schema__()
        self.__create_triggers__()
        self.__add_tasks_by_init__()

    from .__create_schema__ import __create_schema__
    from .__create__triggers__ import __create_triggers__

    from .add import add_tw_subscription
    from .add import add_tw_channel
    from .add import add_tg_chat
    from .add import add_tw_user
    from .add import add_twitch_message
    from .add import __add_tasks_by_init__
    from .add import add_tw_stream
    from .add import add_tw_stream_info

    from .remove import remove_tw_subscription
    from .remove import remove_task_from_channel_actions_deque

    from .get_and_is import get_tw_channel_id_by_name
    from .get_and_is import get_active_stream_id_for_channel
    from .get_and_is import get_tw_user_id_by_name
    from .get_and_is import get_state_for_tg_chat
    from .get_and_is import get_tasks_from_channel_actions_deque
    from .get_and_is import is_tg_chat_has_sub_to_tw_channel
    from .get_and_is import get_listening_channels
    from .get_and_is import get_subscribed_channels
    from .get_and_is import view_msg_qty_for_channel
    from .get_and_is import view_viewers_qty_for_channel

    from .set import set_state_for_tg_chat
