import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import token
from finite_state_machine import Login, Register, Report, Income, Cost
import asyncio

# Logging
logging.basicConfig(level=logging.INFO)

# Initialization
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


# Handler /start command
@dp.message_handler(commands=['start'])
async def start_cmd(message=types.Message):
    user = message.from_user.username
    await message.reply(f'Здравствуйте, {user}!', reply=False)


# Handler /help command
@dp.message_handler(commands=['help'])
async def help_cmd(message=types.Message):
    await message.reply('/login - вход в личный кабинет\n'
                        '/registration - регистрация личного кабинета\n'
                        '/report - отчет о финансах\n'
                        '/income - добавление дохода\n'
                        '/cost - добавление расхода\n'
                        '/accumulation - настройка накоплений\n'
                        '/investment - настройка инвестирования\n'
                        '/donate - "ONLY FOR TESTS", "ТОЛЬКО ДЛЯ ТЕСТОВ" проверка транзакций', reply=False)


# Handler /login command
@dp.message_handler(commands=['login'])
async def login_cmd(message=types.Message):
    await message.reply('Номер телефона:', reply=False)
    await Login.first()


# Handler Login.Telephone state
@dp.message_handler(state=Login.Telephone)
async def login_telephone(message=types.Message, state=FSMContext):
    try:
        await state.update_data(telephone=int(message.text))
        await message.reply('Пароль:', reply=False)
        await Login.next()
    except ValueError:
        await message.reply('Пожалуйста, вводите номер числами.', reply=False)
        await state.finish()


# Handler Login.Password state
@dp.message_handler(state=Login.Password)
async def login_password(message=types.Message, state=FSMContext):
    user = message.from_user.username
    await state.update_data(password=message.text)
    try:
        # Querry to database
        await message.reply(f'Здраввствуйте, {user}!', reply=False)
        await state.finish()
    except BaseException:
        await message.reply('Произошла ошибка, пожалуйста, повтрите попытку входа.', reply=False)


# Handler /register command
@dp.message_handler(commands=['register'])
async def register_cmd(message=types.Message):
    await message.reply('Номер телефона:', reply=False)
    await Register.first()


# Handler Register.Telephone state
@dp.message_handler(state=Register.Telephone)
async def register_telephone(message=types.Message, state=FSMContext):
    await state.update_data(phone_number=message.text)
    await message.reply('Пароль:', reply=False)
    await Register.next()


# Handler Login.Password_first state
@dp.message_handler(state=Register.Password_first)
async def register_password_first(message=types.Message, state=FSMContext):
    await state.update_data(password_1=message.text)
    await message.reply('Пожалуйста, повторите пароль:', reply=False)
    await Register.next()


# Handler Login.Password_second state
@dp.message_handler(state=Register.Password_second)
async def register_password_second(message=types.Message, state=FSMContext):
    await state.update_data(password_2=message.text)
    phone_number = await state.get_data(['phone_number'])
    first_password = await state.get_data(['password_1'])
    second_password = await state.get_data(['password_2'])
    user = message.from_user.username

    if first_password == second_password:
        try:
            # Querry to database
            await message.reply(f'Добро пожаловать, {user}!', reply=False)
        except BaseException:
            await message.reply('Произошла ошибка, пожалуйста, повтрите попытку регистрации.', reply=False)
        finally:
            await state.finish()
    else:
        await message.reply('Пожалуйста, вводите одинаковые пароли, регистрация прошла неудачно.', reply=False)
        await state.finish()


# Handler Report command
@dp.message_handler(commands=['report'])
async def report_cmd(message=types.Message):
    await message.reply('Пожалуйста, введите период отчета: ', reply=False)
    await Report.first()


# Handler Report.date state
@dp.message_handler(state=Report.date)
async def report_date(message=types.Message, state=FSMContext):
    await state.update_data(date=message.text)
    try:
        await state.update_data(date=int(message.text))
        # Query to database
        await message.reply('-', reply=False)
    except ValueError:
        await message.reply('Пожалуйста, вводите дату числами.', reply=False)
    finally:
        await state.finish()


# Handler Income command
@dp.message_handler(commands=['income'])
async def income_cmd(message=types.Message):
    await Income.first()
    await message.reply('Пожалуйста, введите дату вашего дохода:', reply=False)


# Handler Income.date state
@dp.message_handler(state=Income.date)
async def income_date(message=types.Message, state=FSMContext):
    try:
        await state.update_data(date=int(message.text))
        await message.reply('Пожалуйста, выберите категорию дохода:', reply=False)
        await Income.next()
    except ValueError:
        await message.reply('Пожалуйста, введите дату цыфрами.')
        await state.finish()


# Handler Inacome.category state
@dp.message_handler(state=Income.category)
async def income_category(message=types.Message, state=FSMContext):
    await state.update_data(category=message.text)
    await message.reply('Пожалуйста, введите размер дохода:', reply=False)
    await Income.next()


# Handler Income.size state
@dp.message_handler(state=Income.size)
async def income_size(message=types.Message, state=FSMContext):
    try:
        await state.update_data(size=int(message.text))
        data = await state.get_data()
        date = data['date']
        category = data['category']
        size = data['size']
        await message.reply(f'Отлично, Ваш доход размером {size} категории {category} {date} учтен.', reply=False)
    except ValueError:
        await message.reply('Пожалуйста, вводите размер дохода числами.')
    finally:
        await state.finish()


# Handler Cost command
@dp.message_handler(commands=['cost'])
async def cost_cmd(message=types.Message):
    await Cost.first()
    await message.reply('Пожалуйста, введите дату расхода:', reply=False)


# Handler Cost.date state
@dp.message_handler(state=Cost.date)
async def cost_date(message=types.Message, state=FSMContext):
    try:
        await state.update_data(date=int(message.text))
        await message.reply('Пожалуйста, выберите категорию:', reply=False)
        await Cost.next()
    except ValueError:
        await message.reply('Пожалуйста, вводите дату числами.', reply=False)
        await state.finish()


# Handler Cost.category state
@dp.message_handler(state=Cost.category)
async def cost_category(message=types.Message, state=FSMContext):
    await state.update_data(category=message.text)
    await message.reply('Пожалуйста, введите размер расхода', reply=False)
    await Cost.next()


# Handler Cost.size state
@dp.message_handler(state=Cost.size)
async def cost_size(message=types.Message, state=FSMContext):
    try:
        await state.update_data(size=int(message.text))
        data = await state.get_data()
        date = data['date']
        category = data['category']
        size = data['size']
        # Querry to database
        await message.reply(f'Отлично, Ваш расход размером {size} категории {category} {date} учтен.', reply=False)
    except ValueError:
        await message.reply('Пожалуйста, вводите размер расхода числами')
    finally:
        await state.finish()

if True:
    executor.start_polling(dp, skip_updates=True)
