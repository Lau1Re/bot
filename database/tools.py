from database.utils import connect_database


class TableTools:
    def __init__(self, db_path: str = '../database.sqlite3'):
        self.__connection, self.__cursor = connect_database()


class UserTools:
    pass


class AdminTools:
    pass


class AdminCodesTools:
    pass


class FactorTools:
    pass


class DBTools:
    def __init__(self):
        self.admin_tools: AdminTools = AdminTools()
        self.user_tools: UserTools = UserTools()
        self.admin_codes_tools: AdminCodesTools = AdminCodesTools()
        self.factor_tools: FactorTools = FactorTools()
