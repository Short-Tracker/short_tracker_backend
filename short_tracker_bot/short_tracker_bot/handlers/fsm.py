from aiogram import Bot, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .api_data import get_data, get_token

router = Router()


class Login(StatesGroup):
    email = State()
    password = State()
    new_token = State()


@router.message(CommandStart())
async def email(message: types.Message, state: FSMContext):
    await state.update_data(chat_id=message.chat.id)
    await state.set_state(Login.email)
    await message.answer('Введите свою почту')


@router.message(Login.email)
async def password(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(Login.password)
    await message.answer('Введите пароль')
    await message.delete()


@router.message(Login.password)
async def main_func(message: types.Message, state: FSMContext, bot: Bot):
    data_fsm = await state.get_data()
    chat_id = data_fsm['chat_id']
    await state.update_data(password=message.text)
    await get_token(state, chat_id, bot, Login)
    await message.delete()
    await get_data(state, bot)
