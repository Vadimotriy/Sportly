from aiogram import types, F, Router, Bot
from aiogram.filters import Command

from Telegram.database.constants import *
from Telegram.database.functions import make_keyboard, make_keyboard_inline
from Telegram.database.database import User, Session

router = Router()


def handlers(session: Session):
    @router.message(F.text, Command('start'))
    async def start(message: types.Message):
        res = session.query(User).filter(User.id == message.from_user.id).first()
        if not res:
            user = User(id=message.from_user.id)
            session.add(user)
            session.commit()

            keyboard = make_keyboard(['Войти'], 1, message.from_user.id)
            await message.answer(text=start_message, keyboard=keyboard)
        elif not res.logged:
            keyboard = make_keyboard_inline(['Войти'], 1, message.from_user.id)
            await message.answer(text=start_message, reply_markup=keyboard)
        else:
