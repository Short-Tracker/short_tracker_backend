import asyncio

from aiogram import F, Router, Bot
from aiogram import types
from aiogram.filters import CommandStart
from keyboards.keyboards import start_keyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from short_tracker_bot.handlers.requests import request_get, request_post
from short_tracker_bot.config import URL

router = Router()
OLD_MESSAGES = []
OLD_REPLIES = []


class Login(StatesGroup):
    email = State()
    password = State()
    new_token = State()
    refresh_token = State()


async def refresh_token(url, token, state):
    data = {
        'refresh': token
    }
    data = await request_post(url, data)
    token = data.cookies.get('jwt_access').value
    return token


async def get_messages(data, chat_id, bot: Bot):
    for msg in data['results'][0]['messages']:
        if msg['id'] not in OLD_MESSAGES:
            OLD_MESSAGES.append(msg['id'])
            await bot.send_message(
                chat_id,
                text=f'У вас новое сообщение\n\"{msg["message_body"]}\"'
            )
        for reply in msg['reply']:
            if reply['id'] not in OLD_REPLIES:
                OLD_REPLIES.append(reply['id'])
                await bot.send_message(
                    chat_id,
                    text=f'На ваш запрос к лиду поступил ответ:\n{reply["reply_body"]}'
                )


async def get_status(state: FSMContext, bot: Bot):
    data_fsm = await state.get_data()
    token = data_fsm['new_token']
    headers = {
        'Authorization': token
    }
    tasks_dict = dict()
    tasks_expired = []
    while True:
        try:
            data = await request_get(
                URL + 'bot/',
                headers=headers)
            chat_id = data_fsm['chat_id']
            await get_messages(data, chat_id, bot)

            for task in data['results'][0]['tasks_for_user']:
                if task['description'] not in tasks_dict.keys():
                    await bot.send_message(
                        chat_id=chat_id,
                        text=f'У Вас появилась новая задача \"{task["description"]}\"'
                    )
                    tasks_dict[task['description']] = task['status']
                if task['status'] != tasks_dict[task['description']]:
                    tasks_dict[task['description']] = task['status']
                    await bot.send_message(
                        chat_id=chat_id,
                        text=f'Изменен статус задачи \"{task["description"]}\" на {task["status"]}')
                if task['is_expired'] and task['description'] not in tasks_expired:
                    tasks_expired.append(task['description'])
                    performers = [performer['full_name'] for performer in task['performers']]
                    await bot.send_message(
                        chat_id=chat_id,
                        text=f'Задача \"{task["description"]}\" сотрудника'
                             f' {", ".join(performers)} просрочена'
                    )
        except Exception:
            await bot.send_message(data_fsm['chat_id'], 'Произошла ошибка')
        finally:
            await asyncio.sleep(15)


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
    await message.delete()


@router.message(Login.password)
async def get_token(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(password=message.text)
    data_fsm = await state.get_data()
    data = {
        'email': data_fsm['email'],
        'password': data_fsm['password']
    }
    try:
        request = await request_post(
            URL + 'auth/login/',
            data
        )
        token = request.cookies.get('jwt_access')
        refresh_token = request.cookies.get('jwt_refresh')
        if token:
            await state.update_data(new_token=f'Bearer {token.value}')
            data_fsm = await state.get_data()
            await message.delete()
            await state.update_data(refresh_token=f'Bearer {refresh_token.value}')
            await get_status(state, bot)
    except Exception:
        await bot.send_message(data_fsm['chat_id'], 'Нет соединения')
        await message.delete()
