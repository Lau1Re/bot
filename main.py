import asyncio

from parser import Parser


def on_startup():
    # Parser().run()
    pass

if __name__ == '__main__':
    from aiogram.utils import executor
    from handlers import dp

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup())
