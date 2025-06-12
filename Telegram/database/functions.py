from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton

from Telegram.database.constants import BUTTONS, BUTTONS_ADMIN


def make_keyboard(buttons=BUTTONS['buttons'], adjust=BUTTONS['adjust']):
    builder = ReplyKeyboardBuilder()
    for i in buttons:
        builder.add(KeyboardButton(text=i))
    builder.adjust(adjust)

    return builder.as_markup()


def make_keyboard_inline(buttons, adjust, id):
    builder = InlineKeyboardBuilder()
    for i in buttons:
        builder.add(InlineKeyboardButton(text=i, callback_data=f'*{id}'))
    builder.adjust(adjust)

    return builder.as_markup()

