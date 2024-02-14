from aiogram import types, Dispatcher

from config import bot, db, admin_id
from messages import notification_msg
from keyboards import *


async def send_notification(message: types.Message):
    if message.from_user.id == int(admin_id):
        profiles = db.get_all_profiles()

        sent_counter = 0
        for profile in profiles:
            profile_id = profile[1]
            try:
                await bot.send_message(chat_id=profile_id, text=notification_msg, reply_markup=first_start_ikb)
                sent_counter += 1
            except Exception as e:
                print(f'[BOT] Error with sending message to user {profile_id}:', e)

        print(f'[BOT] Notification is sent to {sent_counter} profiles, not sent to: {len(profiles) - sent_counter}')
        await bot.send_message(chat_id=admin_id,
                               text=f'Отправлено. Получили: {sent_counter}. Не получили: {len(profiles) - sent_counter}')


async def ping(message: types.Message):
    if message.from_user.id == int(admin_id):
        print(f'[ADMIN] Bot is active')
        await bot.send_message(admin_id, 'OK')


# ------------------------------------- REGISTER HANDLERS

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(callback=ping, commands=['ping'])
    dp.register_message_handler(callback=send_notification, commands=['send_notification'])
