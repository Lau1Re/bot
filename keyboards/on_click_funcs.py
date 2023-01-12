from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedMultiSelectAdapter, ManagedCheckboxAdapter


class CreatorGroup(StatesGroup):
    OwnMenu = State()
    FactorStatus = State()


class AdminGroup(StatesGroup):
    OwnMenu = State()
    FactorStatus = State()


async def creators_change_status(call: types.CallbackQuery, checkbox: ManagedCheckboxAdapter,
                                 dialog_manager: DialogManager):
    await call.answer()


async def admins_change_status(call: types.CallbackQuery, checkbox: ManagedCheckboxAdapter,
                               dialog_manager: DialogManager):
    await call.answer()
