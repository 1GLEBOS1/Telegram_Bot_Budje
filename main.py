import logging
from aiogram import Bot, Dispatcher, types, exceptions
from configs import token

# Logging
logging.basicConfig(level=logging.INFO)

# Initialization
bot = Bot(token=token)
dp = Dispatcher(bot=bot)


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

if True:
    dp.start_polling()
