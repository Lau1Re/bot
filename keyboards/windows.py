from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo, Checkbox
from aiogram_dialog.widgets.text import Const

from keyboards.on_click_funcs import CreatorGroup, AdminGroup, creators_change_status, admins_change_status


def creators_show_main_menu():
    window = Window(
        Const('🏠 Главное Меню'),
        SwitchTo(Const('✔️ Статус'),
                 id='creators_to_status',
                 state=CreatorGroup.FactorStatus
                 ),
        state=CreatorGroup.OwnMenu

    )

    return window


def creators_show_factory_status():
    window = Window(
        Const('<b>Ваш статус:</b>'),
        Checkbox(Const('✔️ Включён'),
                 Const('✖️ Выключен'),
                 id='creators_show_factory',
                 default=False,
                 on_state_changed=creators_change_status
                 ),
        state=CreatorGroup.FactorStatus
    )

    return window


def admins_show_main_menu():
    window = Window(
        Const('🏠 Главное Меню'),
        SwitchTo(Const('✔️ Статус'),
                 id='admins_to_status',
                 state=AdminGroup.FactorStatus
                 ),
        state=AdminGroup.OwnMenu
    )

    return window


def admins_show_factory_status():
    window = Window(
        Const('<b>Ваш статус:</b>'),
        Checkbox(Const('✔️ Включён'),
                 Const('✖️ Выключен'),
                 id='admins_show_factory',
                 default=False,
                 on_state_changed=admins_change_status
                 ),
        state=AdminGroup.FactorStatus
    )

    return window
