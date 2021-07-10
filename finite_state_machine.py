from aiogram.dispatcher.filters.state import State, StatesGroup


class Login(StatesGroup):
    Telephone = State()
    Password = State()


class Register(StatesGroup):
    Telephone = State()
    Password_first = State()
    Password_second = State()


class Report(StatesGroup):
    date = State()


class Income(StatesGroup):
    date = State()
    category = State()
    size = State()


class Cost(StatesGroup):
    date = State()
    category = State()
    size = State()
