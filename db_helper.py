import sqlite3


class User:
    def __init__(self, telegram_username, telegram_id, telgram_user_first_name, telgram_user_second_name):
        self.telegram_id = telegram_id
        self.telegram_username = telegram_username
        self.telgram_user_first_name = telgram_user_first_name
        self.telgram_user_second_name = telgram_user_second_name


class StandupResponse:
    def __init__(self, user_id, standup_date, commit_date, response):
        self.user_id = user_id
        self.standup_date = standup_date
        self.commit_date = commit_date
        self.response = response


class DatabaseHelper:
    def __init__(self, dbname, workmode='prod'):
        self.conn = sqlite3.connect(dbname)
        self.workmode = workmode
        self.create_tables()


    def create_tables(self):
        cursor = self.conn.cursor()
        if self.workmode != 'prod':
            cursor.execute('DROP TABLE IF  EXISTS standup_responses')
            cursor.execute('DROP TABLE IF  EXISTS developers')

        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS developers (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        telegram_username TEXT,
                        telegram_id INTEGER,
                        telgram_user_first_name TEXT,
                        telgram_user_second_name TEXT,
                        last_standup_date DATE,
                        joined_date  DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS standup_responses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        standup_date DATE,
                        commit_date  default CURRENT_TIMESTAMP,
                        response TEXT,
                        FOREIGN KEY (user_id) REFERENCES developers (user_id)
                    )
                ''')
        self.conn.commit()
        self.conn.close()

    def register_developer(self, user):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT OR REPLACE INTO developers (telegram_username, telegram_id, telgram_user_first_name, telgram_user_second_name) VALUES (?, ?)',
            (user.telegram_username, user.telegram_id, user.telgram_user_first_name, user.telgram_user_second_name))
        self.conn.commit()

    def close(self):
        self.conn.close()
