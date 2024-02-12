import os

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from config import bot, bot_name, db
from .states import ProfileStatesGroup
from messages import *
from keyboards import *
from utils.validators import validate_name, validate_description


async def change_profile(callback: types.CallbackQuery):
    await callback.message.answer(text='<b>🔹Напиши своё имя</b>', reply_markup=cancel_profile_changing_ikb)
    await ProfileStatesGroup.name.set()


async def save_name(message: types.Message, state: FSMContext):
    is_correct_name = await validate_name(message.text)
    if is_correct_name:
        async with state.proxy() as data:
            data['name'] = message.text
        await message.answer(text='<b>🔹Напиши описание для профиля</b>', reply_markup=cancel_profile_changing_ikb)
        await ProfileStatesGroup.next()
    else:
        await message.answer(text='<b>😒 В твоем имени нет букв?</b>\n\n Напиши имя с буквами',
                             reply_markup=cancel_profile_changing_ikb)


async def save_description(message: types.Message, state: FSMContext):
    is_correct_description, sign_qty = await validate_description(message.text)
    if is_correct_description:
        async with state.proxy() as data:
            data['description'] = message.text
        await message.answer(text='<b>🔹Отправь фото</b>', reply_markup=cancel_profile_changing_ikb)
        await ProfileStatesGroup.next()
    else:
        await message.answer(text=f' <b>😒 Ого как много букв в описании</b>\n\n'
                                  f'Должно быть не более 512 символов. У тебя: {sign_qty}. Сократи, пожалуйста',
                             reply_markup=cancel_profile_changing_ikb)


async def save_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    if photo:
        if not os.path.exists(f'media/id{message.from_user.id}'):
            os.mkdir(f'media/id{message.from_user.id}')
        await photo.download(f'media/id{message.from_user.id}/avatar{message.from_user.id}.png')

        async with state.proxy() as data:
            name = data['name']
            description = data['description']
            db.change_profile(user_id=message.from_user.id, name=name, description=description)

        profile_img = types.InputFile(f'media/id{message.from_user.id}/avatar{message.from_user.id}.png')
        await bot.send_photo(message.from_user.id, photo=profile_img)
        await bot.send_message(chat_id=message.from_user.id,
                               text=await get_profile_msg(name, description),
                               reply_markup=profile_ikb)
        await state.finish()

    else:
        await message.answer('Что-то не так. Отправь снова, пожалуйста', reply_markup=cancel_profile_changing_ikb)


async def cancel_profile_changes(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()

    profile = db.get_profile(callback.from_user.id)

    # IF IT IS FIRST START THEN SHOULD TO WRITE PROFILE DATA
    if profile[3]:
        name = profile[3]
        description = profile[4]

        await callback.answer('Отменили')
        profile_img = types.InputFile(f'media/id{callback.from_user.id}/avatar{callback.from_user.id}.png')
        await bot.send_photo(callback.from_user.id, photo=profile_img)
        await bot.send_message(chat_id=callback.from_user.id,
                               text=await get_profile_msg(name, description),
                               reply_markup=profile_ikb)
    else:
        await callback.message.answer('Отменили', reply_markup=first_start_ikb)


async def get_link(callback: types.CallbackQuery):
    profile_id = callback.from_user.id
    profile = db.get_profile(profile_id)

    # IF IT IS FIRST START THEN SHOULD TO WRITE PROFILE DATA
    if not profile[3]:
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Чтобы создать ссылку, нужно указать имя и описание. А ещё загрузить фото. '
                                    'Люди должны знать, кому оставляют валентинку!')
        await callback.message.answer(text='<b>🔹Напиши своё имя</b>', reply_markup=cancel_profile_changing_ikb)
        await ProfileStatesGroup.name.set()
    else:
        url = f'https://t.me/{bot_name}?start=profile{callback.from_user.id}'
        await bot.send_message(chat_id=callback.from_user.id,
                               text=await get_link_msg(url),
                               reply_markup=profile_ikb,
                               disable_web_page_preview=True)


async def get_valentine_cards(callback: types.CallbackQuery):
    valentine_cards = db.get_valentine_cards(callback.from_user.id)

    if valentine_cards:
        await callback.message.answer(text=f'🎉 У тебя уже {len(valentine_cards)} валентинок!')
        for n, card in enumerate(valentine_cards):
            if n == len(valentine_cards)-1:
                await callback.message.answer(text=f'---{n + 1}\n<i>{card[0]}</i>', reply_markup=profile_ikb)
            else:
                await callback.message.answer(text=f'---{n+1}\n<i>{card[0]}</i>')
    else:
        await callback.message.answer('У тебя ещё нет валентинок. Поделись ссылкой в социальных сетях, чтобы люди знали',
                                      reply_markup=profile_ikb)


# ------------------------------------- REGISTER HANDLERS

def register_profile_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(callback=get_link, text=['link'])
    dp.register_callback_query_handler(callback=get_valentine_cards, text=['valentine_cards'])

    dp.register_callback_query_handler(callback=change_profile, text=['change_profile'])
    dp.register_message_handler(callback=save_name, state=ProfileStatesGroup.name)
    dp.register_message_handler(callback=save_description, state=ProfileStatesGroup.description)
    dp.register_message_handler(callback=save_photo, content_types=['photo'], state=ProfileStatesGroup.photo)
    dp.register_callback_query_handler(callback=cancel_profile_changes,
                                       state=ProfileStatesGroup.name,
                                       text=['cancel_profile_changing'])
    dp.register_callback_query_handler(callback=cancel_profile_changes,
                                       state=ProfileStatesGroup.description,
                                       text=['cancel_profile_changing'])
    dp.register_callback_query_handler(callback=cancel_profile_changes,
                                       state=ProfileStatesGroup.photo,
                                       text=['cancel_profile_changing'])
