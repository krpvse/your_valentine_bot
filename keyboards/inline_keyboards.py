from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


first_start_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🌐 Получить свою ссылку', callback_data='link'),
        ],
    ],
    resize_keyboard=True
)


profile_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='✏️ Изменить профиль', callback_data='change_profile'),
        ],
        [
            InlineKeyboardButton(text='❤️ Мои валентинки️', callback_data='valentine_cards'),
            InlineKeyboardButton(text='🌐 Моя ссылка', callback_data='link'),
        ],
    ],
    resize_keyboard=True
)


cancel_profile_changing_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отменить', callback_data='cancel_profile_changing'),
        ],
    ],
    resize_keyboard=True
)


cancel_sending_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Не отправлять', callback_data='cancel_sending'),
        ],
    ],
    resize_keyboard=True
)


async def get_send_valentine_card_ikb(profile_id: int):
    card_to_profile_ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='❤️ Отправить валентинку', callback_data=f'send_valentine_card_to={profile_id}'),
            ],
            [
                InlineKeyboardButton(text='🌐 Получить свою ссылку', callback_data='link'),
            ],

        ],
        resize_keyboard=True
    )
    return card_to_profile_ikb
