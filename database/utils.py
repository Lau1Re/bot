import sqlite3
from config import DATABASE


def connect_database(db_path: str = 'database.sqlite3'):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    return con, cur
