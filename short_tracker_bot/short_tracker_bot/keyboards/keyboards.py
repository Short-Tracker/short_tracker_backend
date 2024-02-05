from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup

keyboard_button = KeyboardButton(text='/войти')

start_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[keyboard_button, ], ]
)
