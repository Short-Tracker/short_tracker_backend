import datetime

from aiogram import F, Router, Bot
from aiogram import types
from aiogram.filters import CommandStart
from keyboards.keyboards import start_keyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import logging
import requests
import time
from short_tracker_bot.config import URL

URLS = {

}

router = Router()


class Login(StatesGroup):
    email = State()
    password = State()
    new_token = State()
    response = State()


async def get_status(state: FSMContext, bot: Bot):
    data_fsm = await state.get_data()
    token = data_fsm['new_token']
    headers = {
        'Authorization': token
    }
    tasks = dict()
    tasks_expired = []
    while True:
        try:
            messages = requests.get(
                URL + 'tasks/',
                headers=headers).json()
            chat_id = data_fsm['chat_id']
            for msg in messages['results']:
                deadline = datetime.datetime.strptime(msg['deadline_date'], '%Y-%m-%d').date()
                if msg['description'] not in tasks.keys():
                    tasks[msg['description']] = msg['status']
                if msg['status'] != tasks[msg['description']]:
                    tasks[msg['description']] = msg['status']
                    await bot.send_message(
                        chat_id=chat_id,
                        text=f'Изменен статус задачи {msg["description"]} на {msg["status"]}')
                if datetime.date.today() > deadline and msg['description'] not in tasks_expired:
                    tasks_expired.append(msg['description'])
                    performers = [performer['full_name'] for performer in msg['performers']]
                    await bot.send_message(
                        chat_id=chat_id,
                        text=f'Задача {msg["description"]} сотрудника'
                             f' {", ".join(performers)} просрочена'
                    )
        except Exception:
            await bot.send_message(data_fsm['chat_id'], 'Произошла ошибка')
        finally:
            time.sleep(15)


@router.message(CommandStart())
async def hello(message: types.Message):
    await message.answer('''Здравствуйте! Я бот трэкера задач
    #https://short-tracker.acceleratorpracticum.ru. Чем я могу Вам помочь?''',
                         reply_markup=start_keyboard)


@router.message(F.text == '/войти')
async def email(message: types.Message, state: FSMContext):
    await state.update_data(chat_id=message.chat.id)
    await state.set_state(Login.email)
    await message.answer('Введите свою почту')


@router.message(Login.email)
async def password(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(Login.password)
    await message.answer('Введите пароль')


@router.message(Login.password)
async def get_token(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(password=message.text)
    data_fsm = await state.get_data()
    data = {
        'email': data_fsm['email'],
        'password': data_fsm['password']
    }
    try:
        get_token = requests.post(
            URL + 'auth/login/',
            data=data
        )
        token = get_token.cookies.get('jwt_access')
        if token:
            await state.update_data(new_token=f'Bearer {token}')
            await state.set_state(Login.response)
            await get_status(state, bot)
        else:
            await message.answer(text='Неверный логин или пароль')
    except Exception:
        await bot.send_message(data_fsm['chat_id'], 'Нет соединения')
