from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime
from datetime import datetime


class BotDb:
    """DB manager class to manage db operations"""

    db_engine = None
    def __init__(self, dbname='bot_db'):
        engine_url = 'sqlite:///db.sqlite3'
        self.db_engine = create_engine(engine_url)

    """Function to create db tables"""
    def create_db_tables(self):
        metadata = MetaData()
        #create history table
        history = Table('history', metadata,
                      Column('id', Integer, primary_key=True, autoincrement=True),
                      Column('username', String),
                      Column('query', String),
                      Column('created_at', DateTime)
                      )
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    def insert_history(self,username,query):
        """insert search history in database"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db_query = f'INSERT into history (username,query,created_at) VALUES ("{username}","{query}","{now}");'
        # print(db_query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(db_query)
                connection.close()
            except Exception as e:
                print(e)

    def fetch_history(self,username,query):
        """fetch recent history from database"""
        res = []
        db_query = f'SELECT * FROM history WHERE username = "{username}" and query like \'%{query}%\' ORDER BY created_at DESC LIMIT 5;'
        # print(db_query)
        with self.db_engine.connect() as connection:
            try:
                res = connection.execute(db_query).fetchall()
                connection.close()
            except Exception as e:
                print(e)
        return res





