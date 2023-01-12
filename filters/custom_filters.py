from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from database.tools import DBTools


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        user_id = message.from_user.id
        admins = DBTools().admin_tools.get_admins_list()
        # print(f'IsAdmin {admins}')

        return user_id in admins


class IsCreator(BoundFilter):
    async def check(self, message: types.Message, inverse: bool = False) -> bool:
        user_id = message.from_user.id
        creators = DBTools().admin_tools.get_creators_list()

        return user_id in creators


class IsDeepLink(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        args = message.get_args()
        return args is not None and len(args) > 0


class IsUser(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        user_id = message.from_user.id
        creators = DBTools().admin_tools.get_creators_list()
        admins = DBTools().admin_tools.get_admins_list()

        return user_id not in creators and user_id not in admins


class IsRegistered(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        user_id = message.from_user.id
        users = DBTools().user_tools.get_users_list()
        return user_id in users
