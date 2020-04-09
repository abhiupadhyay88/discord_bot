import bot_db
import os

os.system('touch db.sqlite3')
dbms = bot_db.BotDb()
dbms.create_db_tables()
