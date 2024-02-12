import asyncio
import logging

from aiogram import Bot, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import HEADERS, URL
from keyboards.keyboards import start_keyboard

from .redis_data import get_data_from_redis, save_data_to_redis
from .requests import request_get, request_post

router = Router()


class Login(StatesGroup):
    email = State()
    password = State()
    new_token = State()


async def get_token(state, bot):
    data_fsm = await state.get_data()
    data = {
        'email': data_fsm['email'],
        'password': data_fsm['password']
    }
    logging.info(f'email, password {data}')
    try:
        request = await request_post(
            URL + 'auth/login/',
            data,
            headers=HEADERS
        )
        logging.info(f'ЗАПРОС ТОКЕНА{request}')
        token = request.cookies.get('jwt_access')
        if token:
            await state.update_data(new_token=f'Bearer {token.value}')
            data_fsm = await state.get_data()
            logging.info(f'NEW TOKEN {data_fsm["new_token"]}')
            await bot.send_message('Вход успешно выполнен!')
            return data_fsm['new_token']
        else:
            await bot.send_message(
                data_fsm['chat_id'],
                'Неверный логин или пароль. Введите пароль еще раз:')
            await state.set_state(Login.email)
    except Exception:
        await bot.send_message(data_fsm['chat_id'], 'Нет соединения')


async def get_messages(data, chat_id, bot: Bot):
    logging.info('Вход в функцию получения сообщений')
    for msg in data['results'][0]['messages']:
        logging.info(msg)
        message_in_redis = await get_data_from_redis(f'{chat_id}_msg_{msg["id"]}')
        logging.info(message_in_redis)
        if not message_in_redis:
            logging.info(message_in_redis)
            await save_data_to_redis(
                f'{chat_id}_msg_{msg["id"]}', msg['message_body']
            )
            await bot.send_message(
                chat_id,
                text=f'У вас новое сообщение\n\"{msg["message_body"]}\"'
            )
        for reply in msg['reply']:
            reply_in_redis = await get_data_from_redis(f'{chat_id}_reply_{msg["id"]}')
            logging.info(reply_in_redis)
            if not reply_in_redis:
                logging.info(reply_in_redis)
                await save_data_to_redis(
                    f'{chat_id}_reply_{msg["id"]}',
                    reply["reply_body"]
                )
                await bot.send_message(
                    chat_id,
                    text=f'На ваш запрос к лиду поступил ответ:'
                         f'\n{reply["reply_body"]}'
                )


async def get_tasks(data, chat_id, bot: Bot):
    for task in data['results'][0]['tasks_for_user']:
        old_task = await get_data_from_redis(f'{chat_id}_task_{task["id"]}')
        logging.info('вход задачи')
        logging.info(old_task)
        if not old_task:
            logging.info(old_task)
            await bot.send_message(
                chat_id=chat_id,
                text=f'У Вас появилась новая задача'
                     f' \"{task["description"]}\"'
            )
            await save_data_to_redis(
                f'{chat_id}_task_{task["id"]}',
                task['status']
            )
        current_status = await get_data_from_redis(
            f'{chat_id}_task_status_{task["id"]}'
        )
        logging.info('вход статус')
        logging.info(current_status)
        if task['status'] != current_status:
            await save_data_to_redis(
                f'{chat_id}_task_status_{task["id"]}',
                task["status"]
            )
            await bot.send_message(
                chat_id=chat_id,
                text=f'Изменен статус задачи '
                     f'\"{task["description"]}\" на {task["status"]}')
        old_data_deadline = await get_data_from_redis(
                f'{chat_id}_status_{task["id"]}'
        )
        logging.info('вход дедлайн')
        logging.info(type(old_data_deadline))
        logging.info(type(task['is_expired']))
        # if task['is_expired']:
        #     logging.info('expired')
        if not old_data_deadline:
            logging.info('dedline')
            await save_data_to_redis(
                f'{chat_id}_status_{task["id"]}',
                ''
            )
            logging.info(task['performers'])
            logging.info(task)
            performers = [performer['full_name'] for performer in task['performers']]
            logging.info('performers')
            await bot.send_message(
                chat_id=chat_id,
                text=f'Задача \"{task["description"]}\" сотрудника'
                     f' {", ".join(performers)} просрочена'
            )


async def get_allows(allows, data, chat_id, bot):
    if allows['notification'] == 'msg' and allows['allow_notification']:
        await get_messages(data, chat_id, bot)
    if allows['notification'] == 'tasks' and allows['allow_notification']:
        await get_tasks(data, chat_id, bot)


async def get_data(state: FSMContext, bot: Bot):
    data_fsm = await state.get_data()
    token = data_fsm['new_token']
    headers = {
        'Authorization': token,
    }
    headers.update(HEADERS)
    chat_id = data_fsm['chat_id']
    logging.info(f'HEADERS {headers}')
    while True:
        try:
            logging.info(URL + 'bot/')
            data = await request_get(
                URL + 'bot/',
                headers=headers)
            logging.info(f'ЗАПРОС ДАННЫХ {data}')
            if data.get('detail'):
                logging.info(f'Запрос токена при истечении срока {token}')
                new_token = await get_token(state, bot)
                headers['Authorization'] = new_token
                logging.info(f'NEW Token {new_token}')
                logging.info(f'New headers {headers}')
                data = await request_get(
                    URL + 'bot/',
                    headers=headers)
            logging.info(f'Запрос сообщений')
            allows = data['allow']
            await get_allows(allows, data, chat_id, bot)
        except Exception:
            logging.error('Не удалось получить данные')
        finally:
            await asyncio.sleep(15)


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
    await state.update_data(password=message.text)
    await get_token(state, bot)
    await message.delete()
    await get_data(state, bot)
