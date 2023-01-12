from aiogram_dialog import Dialog

from keyboards.windows import admins_show_main_menu, creators_show_main_menu, admins_show_factory_status, \
    creators_show_factory_status

AdminDialog = Dialog(
    admins_show_main_menu(),
    admins_show_factory_status()
)

CreatorDialog = Dialog(
    creators_show_main_menu(),
    creators_show_factory_status()
)
