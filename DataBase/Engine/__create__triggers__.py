import sqlite3


def __create_triggers__(self):
    self.cursor.execute("""
                    CREATE TRIGGER IF NOT EXISTS channel_listening_state_set
                        BEFORE INSERT ON ref_tg_tw
                    BEGIN 
                        INSERT INTO tw_channel_actions_deque (action, tw_channel_name)
                        SELECT 'JOIN', tw_channel.name
                        FROM tw_channel
                        WHERE id NOT IN (
                                        select tw_channel_id
                                        from ref_tg_tw
                                    );
                                    
                        UPDATE tw_channel
                        SET IS_LISTENING_STATE = 1
                        WHERE id IN (
                                        select tw_channel_id
                                        from ref_tg_tw
                                    );
                    END
               """)
    self.cursor.execute("""
                    CREATE TRIGGER IF NOT EXISTS channel_listening_state_unset
                        AFTER DELETE ON ref_tg_tw
                    BEGIN 
                        INSERT INTO tw_channel_actions_deque (action, tw_channel_name)
                        SELECT 'LEAVE', tw_channel.name
                        FROM tw_channel
                        WHERE id NOT IN (
                                        select tw_channel_id
                                        from ref_tg_tw
                                    );
                        
                        UPDATE tw_channel
                        SET IS_LISTENING_STATE = 0
                        WHERE id NOT IN (
                                        select tw_channel_id
                                        from ref_tg_tw
                                    );
                    END
               """)
    self.db.commit()
