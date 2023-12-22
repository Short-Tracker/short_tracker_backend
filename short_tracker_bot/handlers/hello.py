from aiogram import F, Router
from aiogram import types
from short_tracker.users.models import CustomUser
from django.shortcuts import

router = Router()


@router.message(F.text == '/start')
async def hello(message: types.Message):
    await message.answer('''Здравствуйте! Я бот трэкера задач
    #https://short-tracker.acceleratorpracticum.ru. Чем я могу Вам помочь?''')
