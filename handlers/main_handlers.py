from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from config import bot, db, admin_id
from messages import get_profile_msg, help_msg
from keyboards import *
from .states import SendValentineCardStatesGroup
from utils.validators import validate_valentine_card


async def start(message: types.Message):
    print(f'[BOT] User {message.from_user.id} starts bot')

    db.add_user(user_id=message.from_user.id)

    args = message.get_args()
    # IF START TO SEND VALENTINE CARD (WITH ARGS)
    if args:
        try:
            profile_id = int(args.replace('profile', ''))
            print(f'[BOT] User {message.from_user.id} is looking profile {profile_id}')
            profile = db.get_profile(profile_id)
        except Exception as e:
            profile = None
            print(f'[BOT] Some problems with "profile_id" in start command by user {message.from_user.id}, error: ', e)

        if profile[3]:
            name = profile[3]
            description = profile[4]

            profile_img = types.InputFile(f'media/id{profile_id}/avatar{profile_id}.png')
            await bot.send_photo(message.from_user.id, photo=profile_img)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=await get_profile_msg(name, description))
            await bot.send_message(chat_id=message.from_user.id,
                                   text='<b>💌 Чтобы отправить валентинку, жми на кнопку клавиатуры ниже</b>',
                                   reply_markup=await get_send_valentine_card_ikb(profile_id))
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Не удается найти профиль. Проверь, пожалуйста, ссылку',
                                   reply_markup=first_start_ikb)
    # IF START TO CREATE PROFILE (WITHOUT ARGS)
    else:
        profile_id = message.from_user.id
        profile = db.get_profile(profile_id)

        # IF IT IS FIRST START THEN SHOULD TO WRITE PROFILE DATA
        if not profile[3]:
            profile_img = types.InputFile('media/start-img.png')
            await bot.send_photo(message.from_user.id, photo=profile_img)
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Привет! Это бот для анонимного получения валентинок. Делись ссылкой в социальных сетях и жди валентинки ❤️',
                                   reply_markup=first_start_ikb)
            await message.delete()

        else:
            name = profile[3]
            description = profile[4]

            profile_img = types.InputFile(f'media/id{profile_id}/avatar{profile_id}.png')
            await bot.send_photo(message.from_user.id, photo=profile_img)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=await get_profile_msg(name, description),
                                   reply_markup=profile_ikb)

    await bot.send_message(admin_id, f'Новый подписчик!\n'
                                     f'id: {message.from_user.id}\n'
                                     f'имя: {message.from_user.full_name}')


async def send_valentine_card(callback: types.CallbackQuery, state: FSMContext):
    profile_id = int(callback.data.replace('send_valentine_card_to=', ''))
    await callback.message.answer(text='<b>💌 Отправь сообщение с валентинкой. Да-да, просто отправь сообщение, и оно сразу отправится</b>\n\n'
                                       '<i>Сообщение анонимно. Если хочешь указать, от кого эта валентинка - напиши это в тексте сам</i>',
                                  reply_markup=cancel_sending_ikb)
    async with state.proxy() as data:
        data['profile_id'] = profile_id
    await SendValentineCardStatesGroup.message.set()


async def send_message(message: types.Message, state: FSMContext):
    print(f'[BOT] User {message.from_user.id} is trying to send valentine card')
    is_correct_valentine_card, sign_qty = await validate_valentine_card(message.text)
    if is_correct_valentine_card:
        async with state.proxy() as data:
            profile_id = data['profile_id']

        valentine_card = message.text
        db.save_valentine_card(profile_id, valentine_card)
        await bot.send_message(chat_id=profile_id, text=f'🎉 У вас новая валентинка!\n\n{valentine_card}', reply_markup=profile_ikb)

        await message.answer(text='✔️ Валентинка отправлена', reply_markup=first_start_ikb)
        print(f'[BOT] User {message.from_user.id} is sent valentine card to profile {profile_id}')
        await state.finish()
    else:
        await message.answer(text=f' <b>😔 Ого как много, придется немного сократить</b>\n\n'
                                  f'Должно быть не более 512 символов. У тебя: {sign_qty}. Сократи, пожалуйста',
                             reply_markup=cancel_profile_changing_ikb)


async def cancel_valentine_card_sending(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        profile_id = data['profile_id']

    profile = db.get_profile(profile_id)

    name = profile[3]
    description = profile[4]

    profile_img = types.InputFile(f'media/id{profile_id}/avatar{profile_id}.png')
    await bot.send_photo(callback.from_user.id, photo=profile_img)
    await bot.send_message(chat_id=callback.from_user.id,
                           text=await get_profile_msg(name, description),
                           reply_markup=await get_send_valentine_card_ikb(profile_id))

    await state.finish()
    print(f'[BOT] User {callback.from_user.id} is cancel valentine card sending')
    await callback.answer('Отправка отменена')


async def get_bot_info(message: types.Message):
    print(f'[BOT] User {message.from_user.id} clicked on "/help"')
    await message.answer(text=help_msg, reply_markup=first_start_ikb)


async def delete_other_messages(message: types.Message):
    print(f'[BOT] User {message.from_user.id} is sent unknown message:\n{message.text}')
    await bot.send_message(admin_id, f'{message.text} / {message.from_user.username} / {message.from_user.full_name}')
    await message.delete()


# ------------------------------------- REGISTER HANDLERS

def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(callback=start, commands=['start'])
    dp.register_message_handler(callback=get_bot_info, commands=['help'])
    dp.register_message_handler(callback=delete_other_messages)

    dp.register_callback_query_handler(callback=send_valentine_card, text_startswith=['send_valentine_card_to'])
    dp.register_message_handler(callback=send_message, state=SendValentineCardStatesGroup.message)
    dp.register_callback_query_handler(callback=cancel_valentine_card_sending,
                                       state=SendValentineCardStatesGroup.message)
