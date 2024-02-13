from aiogram.types import BotCommand

TOKEN = '6787434498:AAHW5Y2gUJQLqttiQ-Vj9qulyBoTCHYYVu4'
URL = 'https://short-tracker.acceleratorpracticum.ru/api/v1/'
COMMANDS = [BotCommand(command='/start', description='Запуск бота')
            ]
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
}
