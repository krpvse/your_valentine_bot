from aiogram.types import BotCommand

from config import bot


async def set_menu():
    bot_commands = [
        BotCommand(command='/start', description='Запустить/перезапустить бот'),
        BotCommand(command='/help', description='Узнать, как пользоваться ботом')
    ]
    await bot.set_my_commands(bot_commands)
