import sqlite3
from typing import Any

from config import DATABASE


def connect_database(db_path: str = 'database.sqlite3') -> tuple[Any, Any]:
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    return connection, cursor
