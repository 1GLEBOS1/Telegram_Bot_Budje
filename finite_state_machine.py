from aiogram.dispatcher.filters.state import State, StatesGroup


class Login(StatesGroup):
    Telephone = State()
    Password = State()
    Output = State()
