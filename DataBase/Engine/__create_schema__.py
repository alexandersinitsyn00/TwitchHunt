import sqlite3


def __create_schema__(self):
    # TWITCH CHANNEL
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS tw_channel 
                      (   ID INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT unique,
                          IS_LISTENING_STATE INTEGER
                      )
                   """)

    # TWITCH STREAM
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS tw_stream
                      (   ID INTEGER PRIMARY KEY,
                          channel_id INTEGER NOT NULL,
                          datetime_begin,
                      FOREIGN KEY(channel_id) REFERENCES tw_channel(ID)
                      )
                    """)

    # TWITCH STREAM HISTORY
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS tw_stream_history
                      (   ID INTEGER PRIMARY KEY,
                          stream_id INTEGER NOT NULL,
                          viewers_count INTEGER,
                          datetime_create,
                      FOREIGN KEY(stream_id) REFERENCES tw_stream(ID)
                      )
                    """)

    # TWITCH USER
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS tw_user 
                      (   ID INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT unique
                      )
                   """)

    # TWITCH_CHAT
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS tw_chat
                      (   ID INTEGER PRIMARY KEY AUTOINCREMENT,
                          stream_id INTEGER NOT NULL,
                          user_id INTEGER NOT NULL,
                          msg TEXT,
                          datetime_create,
                      FOREIGN KEY(stream_id) REFERENCES tw_channel(ID),
                      FOREIGN KEY(user_id) REFERENCES tw_user(ID)
                      )
                   """)

    # TELEGRAM CHAT
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS tg_chat
                      (   ID INTEGER PRIMARY KEY,
                          first_name unique,
                          last_name TEXT,
                          user_name TEXT,
                          language_code TEXT,
                          STATE INTEGER DEFAULT 0
                      )
                   """)

    # REFERENCE: M TG_CHAT - M TW_CHANNEL
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS ref_tg_tw
                      (   ID INTEGER PRIMARY KEY AUTOINCREMENT,
                          tg_chat_id INTEGER NOT NULL,
                          tw_channel_id INTEGER NOT NULL,
                          UNIQUE(tg_chat_id, tw_channel_id),
                      FOREIGN KEY(tw_channel_id) REFERENCES tw_channel(ID),
                      FOREIGN KEY(tg_chat_id) REFERENCES tg_chat(ID)
                      )
                   """)

    # TWITCH CHANNELS ACTIONS DEQUE ( FILLING ONLY BY TRIGGERS )
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS tw_channel_actions_deque
                      (   ID INTEGER PRIMARY KEY AUTOINCREMENT,
                          action TEXT NOT NULL,
                          tw_channel_name TEXT
                      )
                   """)
