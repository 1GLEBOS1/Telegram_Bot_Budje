import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from configs import token
from finite_state_machine import Login, Register

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
    await message.reply(f'Здравствуйте, {user}', reply=False)


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
async def login_cmd(message=types.Message, state=FSMContext):
    await message.reply('Номер телефона:', reply=False)
    await Login.first()


# Handler Login.Telephone state
@dp.message_handler(state=Login.Telephone)
async def login_telephone(message=types.Message, state=FSMContext):
    await state.update_data(telephone=message.text)
    await message.reply('Пароль:', reply=False)
    await Login.next()


# Handler Login.Password state
@dp.message_handler(state=Login.Password)
async def login_password(message=types.Message, state=FSMContext):
    user = message.from_user.username
    await state.update_data(password=message.text)
    try:
        # Querry to database
        await message.reply(f'Здраввствуйте, {user}', reply=False)
        await state.finish()
    except BaseException:
        await message.reply('Произошла ошибка, пожалуйста, повтрите попытку входа', reply=False)


# Handler /register command
@dp.message_handler(commands=['register'])
async def register_cmd(message=types.Message, state=FSMContext):
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
    await message.reply('Пожалуйста, повторите пароль', reply=False)
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
            await message.reply(f'Добро пожаловать, {user}', reply=False)
            await state.finish()
        except BaseException:
            await message.reply('Произошла ошибка, пожалуйста, повтрите попытку регистрации', reply=False)
            await state.finish()

    else:
        await message.reply('Пожалуйста, вводите одинаковые пароли, регистрация прошла неудачно', reply=False)
        await state.finish()

if True:
    executor.start_polling(dp, skip_updates=True)
