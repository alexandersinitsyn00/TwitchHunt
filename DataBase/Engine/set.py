import sqlite3


def set_state_for_tg_chat(self, chat_id, state):
    self.cursor.execute("""UPDATE tg_chat
                                SET STATE = ?
                                WHERE id = ?
    """, (state, chat_id))
    self.db.commit()
