import asyncio

from keyboards.dialogs import AdminDialog, CreatorDialog
from parser import Parser


def on_startup():
    # Parser().run()
    pass

if __name__ == '__main__':
    from aiogram.utils import executor
    from handlers import dp
    from aiogram_dialog import DialogRegistry

    registry = DialogRegistry(dp)
    registry.register(AdminDialog)
    registry.register(CreatorDialog)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup())
