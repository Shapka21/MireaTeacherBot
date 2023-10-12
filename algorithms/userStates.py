from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    ChoseName = State()
    RequestSearchName = State()
