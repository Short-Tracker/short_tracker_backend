from aiogram import F, Router
from aiogram import types
from keyboards.keyboards import start_keyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import requests
router = Router()


class Login(StatesGroup):
    email = State()
    password = State()
    new_token = State()


@router.message(F.text == '/start')
async def hello(message: types.Message):
    await message.answer('''Здравствуйте! Я бот трэкера задач
    #https://short-tracker.acceleratorpracticum.ru. Чем я могу Вам помочь?''',
                         reply_markup=start_keyboard)


@router.message(F.text == '/войти')
async def email(message: types.Message, state: FSMContext):
    await state.set_state(Login.email)
    await message.answer('Введите свою почту')


@router.message(Login.email)
async def password(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(Login.password)
    await message.answer('Введите пароль')


@router.message(Login.password)
async def get_token(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data_fsm = await state.get_data()
    data = {
        'email': data_fsm['email'],
        'password': data_fsm['password']
    }
    get_token = requests.post(
        'http://127.0.0.1:8000/api/v1/auth/jwt/create/',
        data=data
    )

    await state.update_data(new_token=get_token.json())
    data_fsm = await state.get_data()




