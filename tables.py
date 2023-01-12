import config
from database.tools import DBTools
from database.utils import connect_database


class InitDB:
    def __init__(self):
        self.__connection, self.__cursor = connect_database(db_path=config.DATABASE)

    def __create_users_table(self):
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            first_name TEXT NOT NULL,
            last_name TEXT DEFAULT '',
            username TEXT NOT NULL DEFAULT '@username'

        )""")

    def __create_admins_table(self):
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER NOT NULL UNIQUE,
            user_id INTEGER REFERENCES users(id),
            status VARCHAR(7) NOT NULL DEFAULT 'ADMIN' 
            CHECK (status in ('ADMIN', 'CREATOR'))
            
            
        )""")

    def __create_factors_table(self):
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS factors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            factor VARCHAR(10) NOT NULL
             
        )""")

    def __create_admin_codes_table(self):
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS admin_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code VARCHAR(11) NOT NULL UNIQUE,
            status VARCHAR(7) NOT NULL DEFAULT 'ADMIN'
            CHECK (status in ('ADMIN', 'CREATOR'))
        
        )""")


    def init(self):
        self.__create_users_table()
        self.__create_admins_table()
        self.__create_factors_table()
        self.__create_admin_codes_table()
        DBTools().admin_codes_tools.generate_admin_code(status='CREATOR')


if __name__ == '__main__':
    InitDB().init()
