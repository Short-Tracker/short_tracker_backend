import logging

from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardBuilder
from handlers.api_data import get_buttons

keyboard_button = KeyboardButton(text='/start')

start_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[keyboard_button, ], ]
)
