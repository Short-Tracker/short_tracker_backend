import asyncio
import logging

import aiohttp
from aiogram import Bot
from aiogram.fsm.context import FSMContext

from config import HEADERS, URL
from handlers.redis_data import get_data_from_redis, save_data_to_redis
from handlers.requests import request_get, request_post


async def get_token(state, chat_id, bot, new_state):
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
            await bot.send_message(
                chat_id=chat_id,
                text='Вход успешно выполнен!')
            return data_fsm['new_token']
        else:
            await bot.send_message(
                data_fsm['chat_id'],
                'Неверный логин или пароль. Введите пароль еще раз:')
            await state.set_state(new_state)
    except aiohttp.ClientResponseError as e:
        logging.error(f'Ошибка при получении данных: {e}')


async def get_messages(data, chat_id, bot: Bot):
    for msg in data['messages']:
        logging.info(f'MESSAGE {msg}')
        message_in_redis = await get_data_from_redis(
            f'{chat_id}_msg_{msg["id"]}'
        )
        logging.info(f'СООБЩЕНИЕ В БАЗЕ{message_in_redis}')
        if not message_in_redis:
            await save_data_to_redis(
                f'{chat_id}_msg_{msg["id"]}', msg['message_body']
            )
            await bot.send_message(
                chat_id,
                text=f'У вас новое сообщение\n\"{msg["message_body"]}\"'
            )
        for reply in msg['reply']:
            logging.info(f'ENTRY REPLY {reply}')
            reply_in_redis = await get_data_from_redis(
                f'{chat_id}_reply_{msg["id"]}'
            )
            if not reply_in_redis:
                await save_data_to_redis(
                    f'{chat_id}_reply_{msg["id"]}',
                    reply["reply_body"]
                )
                await bot.send_message(
                    chat_id,
                    text=f'На ваш запрос к лиду поступил ответ:'
                         f'\n{reply["reply_body"]}'
                )


async def get_tasks(task, chat_id, bot: Bot):
    old_task = await get_data_from_redis(f'{chat_id}_task_{task["id"]}')
    logging.info('вход задачи')

    if not old_task:
        logging.info('Задача отсутствует в базе')
        await bot.send_message(
            chat_id=chat_id,
            text=f'У Вас появилась новая задача'
                 f' \"{task["description"]}\"'
        )
        logging.info('Отправили сообщение о новой задачк')
        await save_data_to_redis(
            f'{chat_id}_task_{task["id"]}',
            task['status']
        )
        logging.info('Сохранили в базу')


async def get_status(task, chat_id, bot: Bot):
    logging.info('вход статус')
    current_status = await get_data_from_redis(
        f'{chat_id}_task_status_{task["id"]}')
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


async def get_deadline(task, chat_id, bot: Bot):
    old_data_deadline = await get_data_from_redis(
        f'{chat_id}_status_{task["id"]}'
    )
    if task['is_expired'] and not old_data_deadline:
        logging.info('expired')
        logging.info('dedline')
        await save_data_to_redis(
            f'{chat_id}_status_{task["id"]}',
            f'{task["deadline_date"]}_{chat_id}'
        )
        logging.info('save deadline to redis')
        logging.info(task)
        performers = [
            performer['first_name'] for performer in task['performers']
        ]
        logging.info('performers')
        await bot.send_message(
            chat_id=chat_id,
            text=f'Задача \"{task["description"]}\" сотрудника'
                 f' {", ".join(performers)} просрочена'
        )


async def get_allows(allows, data, chat_id, bot):
    if allows['notification'] == 'msg' and allows['allow_notification']:
        logging.info(
            f'Entry msg {allows["notification"]} '
            f'{allows["allow_notification"]}'
        )
        await get_messages(data, chat_id, bot)
    if allows['notification'] == 'status' and allows['allow_notification']:
        logging.info(
            f'Entry status {allows["notification"]}'
            f' {allows["allow_notification"]}'
        )
        for task in data['tasks_for_user']:
            await get_status(task, chat_id, bot)
    if allows['notification'] == 'deadline' and allows['allow_notification']:
        logging.info(
            f'Entry deadline {allows["notification"]} '
            f'{allows["allow_notification"]}'
        )
        for task in data['tasks_for_user']:
            await get_deadline(task, chat_id, bot)
    if allows['notification'] == 'tasks' and allows['allow_notification']:
        logging.info(
            f'Entry tasks {allows["notification"]} '
            f'{allows["allow_notification"]}'
        )
        for task in data['tasks_for_user']:
            logging.info(f'task for {task}')
            await get_tasks(task, chat_id, bot)


async def get_data(state: FSMContext, bot: Bot):
    data_fsm = await state.get_data()
    token = data_fsm['new_token']
    headers = {
        'Authorization': token,
    }
    headers.update(HEADERS)
    chat_id = data_fsm['chat_id']
    while True:
        try:
            data = await request_get(
                URL + 'bot/',
                headers=headers)
            if data.get('detail'):
                logging.info(f'Запрос токена при истечении срока {token}')
                new_token = await get_token(state, bot, chat_id)
                headers['Authorization'] = new_token
                data = await request_get(
                    URL + 'bot/',
                    headers=headers)
            allows = data['results'][0]['allow']
            data = data['results'][0]
            for allow in allows:
                await get_allows(allow, data, chat_id, bot)
        except aiohttp.ClientResponseError as e:
            logging.error(f'Ошибка при получении данных: {e}')
        finally:
            await asyncio.sleep(15)
