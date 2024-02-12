import asyncio
from aiogram import executor

from config import bot, dp, admin_id
from handlers import register_handlers
from keyboards import set_menu


async def on_startup(dp):
    print('Bot is starting')

    await asyncio.sleep(5)
    try:
        await bot.send_message(admin_id, '[ADMIN] Bot is starting')
    except Exception as e:
        print('Error with sending notifications to admin: ', e)
        print('Check out connection with bot or admin id in settings')

    await set_menu()


if __name__ == '__main__':
    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
