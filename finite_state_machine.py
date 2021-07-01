from aiogram.dispatcher.filters.state import State, StatesGroup


class Login(StatesGroup):
    Telephone = State()
    Password = State()


class Register(StatesGroup):
    Telephone = State()
    Password_first = State()
    Password_second = State()
