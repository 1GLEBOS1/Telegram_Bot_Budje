import logging
from aiogram import Bot, Dispatcher, types, exceptions
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from configs import token
from finite_state_machine import Login

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
    await state.update_data(password=message.text)
    await Login.next()


# Handler Login.Output state
@dp.message_handler(state=Login.Output)
async def login_output(message=types.Message, state=FSMContext):
    try:
        # Querry to database
        await message.reply(f'Здраввствуйте, {"Имя"}', reply=False)
    except BaseException:
        await message.reply('Произошла ошибка, пожалуйста, повтрите попытку входа', reply=False)


if True:
    dp.start_polling()
