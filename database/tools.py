import random

import config
from database.utils import connect_database
import string


class TableTools:
    def __init__(self, db_path: str = config.DATABASE):
        self.connection, self.cursor = connect_database(db_path=db_path)


class UserTools(TableTools):
    def register_user(self, user_id: int, first_name: str, last_name: str, username: str | None = None) -> bool | tuple[int]:

        try:
            self.cursor.execute(""" INSERT INTO users (user_id, first_name, last_name, username) 
                                    VALUES (?, ?, ?, ?)
                                  
                                    RETURNING id
                                    """, (user_id, first_name, last_name, username))
        except Exception as err:
            print("ERROR", err)
            return False
        else:
            print('SUCCESS USER INSERT')
            result = self.cursor.fetchone()
            return result

        finally:
            self.connection.commit()
            self.connection.close()

    def is_registered_user(self, user_id: int) -> bool | int:
        self.cursor.execute("""SELECT id
                            FROM users 
                            WHERE user_id = ?
                            """, (user_id,))
        user = self.cursor.fetchone()
        if user:
            return user[0]
        return 0

    def get_users_list(self) -> list[tuple]:
        self.cursor.execute("""SELECT user_id
                                FROM users 
                                """)

        result = self.cursor.fetchall()
        if len(result):
            users = [i[0] for i in result]
            return users

        self.connection.close()
        return result



class AdminTools(TableTools):
    def register_admin(self, admin_id: int, user_id: int, status: str = 'ADMIN') -> bool:

        try:
            self.cursor.execute(""" INSERT INTO admins (admin_id, user_id, status) 
                        VALUES (?, ?, ?)""", (admin_id, user_id, status))
        except Exception as err:
            print("ERROR", err)
            return False
        else:
            print('SUCCESS ADMIN INSERT')
            return True
        finally:
            self.connection.commit()
            self.connection.close()

    def get_admins_list(self) -> list[tuple]:
        self.cursor.execute("""SELECT admin_id
                                FROM admins
                                WHERE status = 'ADMIN'
                                """)

        result = self.cursor.fetchall()
        if len(result):
            admins = [i[0] for i in result]
            return admins

        self.connection.close()
        return result

    def get_creators_list(self) -> list[tuple]:
        self.cursor.execute("""SELECT admin_id
                                FROM admins
                                WHERE status = 'CREATOR' 
                                """)

        result = self.cursor.fetchall()
        if len(result):
            creators = [i[0] for i in result]
            return creators

        self.connection.close()
        return result


class AdminCodesTools(TableTools):
    def generate_admin_code(self, status: str = 'ADMIN') -> str:
        alphabet: str = string.ascii_lowercase + string.digits
        code = [random.choice(alphabet) for i in range(6)]
        code = 'code_' + ''.join(code)

        try:
            self.cursor.execute(""" INSERT INTO admin_codes (code, status) 
                        VALUES (?, ?)
                        """, (code, status))
        except Exception as err:
            print("ERROR", err)
            return ' не был сгенерирован. В аргументы к команде можно передавать только ADMIN или CREATOR'
        else:
            print('SUCCESS CODE GENERATED')
            return code
        finally:
            self.connection.commit()
            self.connection.close()

    def check_code(self, code: str) -> bool | tuple[str, str]:
        try:
            self.cursor.execute("""
                    SELECT code, status
                    FROM admin_codes
                    WHERE code = ?
                    
            """, (code,))
        except Exception as err:
            print(err)
        else:
            result = self.cursor.fetchone()
            if not result:
                return False
            return result

        finally:
            self.connection.close()

    def delete_code(self, code: str) -> bool | str:
        try:
            self.cursor.execute("""
                DELETE FROM admin_codes
                WHERE code = ?
                
            
            """, (code,))
        except Exception as err:
            print(err)
        else:
            result = self.cursor.fetchone()
            if not result:
                return False
            return result[0]
        finally:
            self.connection.commit()
            self.connection.close()

class FactorTools(TableTools):
    def insert_factor(self, factor: str) -> bool:
        try:
            self.cursor.execute(""" INSERT INTO factors (factor) 
                        VALUES (?)""", (factor,))
        except Exception as err:
            print("ERROR", err)
            return False
        else:
            print('SUCCESS factor INSERT')
            return True
        finally:
            self.connection.commit()
            self.connection.close()


class DBTools:
    def __init__(self):
        self.admin_tools: AdminTools = AdminTools()
        self.user_tools: UserTools = UserTools()
        self.admin_codes_tools: AdminCodesTools = AdminCodesTools()
        self.factor_tools: FactorTools = FactorTools()
