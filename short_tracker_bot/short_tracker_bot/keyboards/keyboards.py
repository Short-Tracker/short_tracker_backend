from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


keyboard_button = KeyboardButton(text='/войти')

start_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[keyboard_button, ], ]
)
