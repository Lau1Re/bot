from re import compile

from aiogram import types
from aiogram.dispatcher.filters import Command, CommandStart

from config import dp
from database.tools import DBTools
from filters.custom_filters import IsAdmin, IsCreator, IsDeepLink, IsUser, IsRegistered


@dp.message_handler(IsCreator(), commands=['start'])
async def creator_simple_start(message: types.Message):
    await message.answer('Привет, создатель!')


@dp.message_handler(IsCreator(), IsDeepLink(), CommandStart(deep_link=compile(r'^code_[\d\w]{6}$')))
async def creator_start_with_deeplink(message: types.Message):
    await message.answer(
        f'Привет, создатель! Вы уже имеете максимальные права. Аргумент {message.get_args()} не распознан')


@dp.message_handler(IsAdmin(), commands=['start'])
async def admin_simple_start(message: types.Message):
    await message.answer('Привет, админ!')


@dp.message_handler(IsAdmin(), IsRegistered(), IsDeepLink(), CommandStart(deep_link=compile(r'^code_[\d\w]{6}$')))
async def admin_start_with_deeplink(message: types.Message):
    args = message.get_args()
    args = args.strip()


    status: tuple[str, str] = DBTools().admin_codes_tools.check_code(args)
    if not status:
        await message.answer('Данный код недействителен!')
    else:
        code, admin_status = status

        if admin_status == 'CREATOR':
            user_id = DBTools().user_tools.is_registered_user(message.from_user.id)

            DBTools().admin_tools.register_admin(message.from_user.id,
                                                 user_id=user_id,
                                                 status=admin_status)
            DBTools().admin_codes_tools.delete_code(code)


@dp.message_handler(IsUser(), IsRegistered(), CommandStart(deep_link=compile(r'^code_[\d\w]{6}$')))
async def registered_user_start_with_deeplink(message: types.Message):
    args = message.get_args()
    args = args.strip()

    if args.startswith('code_') and len(args) == 11:
        status: False | tuple[str, str] = DBTools().admin_codes_tools.check_code(args)
        if not status:
            await message.answer('Данный код недействителен!')
        else:
            code, admin_status = status
            user_id = DBTools().user_tools.is_registered_user(message.from_user.id)

            DBTools().admin_tools.register_admin(message.from_user.id,
                                                 user_id=user_id,
                                                 status=admin_status)
            await message.answer(f'Ты зарегистрирован как админ\nПрава: {admin_status}')
            DBTools().admin_codes_tools.delete_code(code)
    else:
        print(args)
        await message.answer(f'Недействительный код активации. Для получения кода обратитесь к @JesseCodes')


@dp.message_handler(IsUser(), CommandStart(deep_link=compile(r'^code_[\d\w]{6}$')))
async def not_registered_user_start_with_deeplink(message: types.Message):
    # await register_and_return(message)

    username = message.from_user.username if message.from_user.username else '@username'

    DBTools().user_tools.register_user(message.from_user.id,
                                       message.from_user.first_name,
                                       message.from_user.last_name,
                                       username)
    await registered_user_start_with_deeplink(message)



@dp.message_handler(IsRegistered(), CommandStart())
async def registered_user_simple_start(message: types.Message):
    await message.answer('И снова здравствуй, новичок!')


@dp.message_handler(CommandStart(deep_link=None))
async def not_registered_start_simple_start(message: types.Message):
    username = message.from_user.username if message.from_user.username else '@username'

    DBTools().user_tools.register_user(message.from_user.id,
                                       message.from_user.first_name,
                                       message.from_user.last_name,
                                       username)
    await message.answer('Привет, я бот который поможет тебе получать коэффициенты!')


@dp.message_handler(IsCreator(), IsRegistered(), commands=['generate'])
async def creator_generate_code(message: types.Message):
    status = message.get_args().strip()
    if not len(status):
        status = 'ADMIN'
    code = DBTools().admin_codes_tools.generate_admin_code(status=status)
    bot = await dp.bot.get_me()
    bot_username = bot.username
    await message.answer(f'Сгенерирован <b>новый код:</b> <code>{code}</code>'
                         f'\nАктивировать можно по ссылке:'
                         f'\nt.me/{bot_username}?start={code}')
