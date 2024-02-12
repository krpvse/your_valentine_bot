from aiogram.dispatcher.filters.state import StatesGroup, State


class ProfileStatesGroup(StatesGroup):
    name = State()
    description = State()
    photo = State()


class SendValentineCardStatesGroup(StatesGroup):
    message = State()
