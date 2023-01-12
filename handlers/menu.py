from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram_dialog import DialogManager, StartMode

from config import dp
from filters.custom_filters import IsRegistered, IsAdmin, IsCreator
from keyboards.on_click_funcs import CreatorGroup, AdminGroup


@dp.message_handler(IsAdmin(), IsRegistered(), Command('menu'))
async def admin_start_with_deeplink(message: types.Message, dialog_manager: DialogManager):


    await dialog_manager.start(AdminGroup.OwnMenu, mode=StartMode.RESET_STACK)


@dp.message_handler(IsCreator(), IsRegistered(), Command('menu'))
async def admin_start_with_deeplink(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(CreatorGroup.OwnMenu, mode=StartMode.RESET_STACK)
