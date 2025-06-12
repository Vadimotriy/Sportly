from aiogram import types, F, Router

from Telegram.database.constants import *
from Telegram.database.database import User
from Telegram.database.functions import make_keyboard
from Telegram.flask_api.flask_api import *

router_for_admin = Router()


def admin(session, bot):
    @router_for_admin.message(F.text == '⚙️АДМИН ПАНЕЛЬ⚙️')
    async def admin_start(message: types.Message):
        if str(message.from_user.id) == ADMINS:
            keyboard = make_keyboard(BUTTONS_ADMIN['buttons'], BUTTONS_ADMIN['adjust'])
            await message.answer('Вы вошли в Админ панель!', reply_markup=keyboard)
        else:
            await message.answer('Вы не админ!!!')

    @router_for_admin.message(F.text == 'Вернуться')
    async def admin_start(message: types.Message):
        if str(message.from_user.id) == ADMINS:
            res = session.query(User).filter(User.id == message.from_user.id).first()
            text = start_message_logged + str(get_name(res.flask)) + '.'
            keyboard = make_keyboard(BUTTONS['buttons'] + ADMIN_BTN, adjust=1)
            await message.answer(text=text, reply_markup=keyboard)
        else:
            await message.answer('Вы не админ!!!')

    @router_for_admin.message(F.text == 'Сделать рассылку')
    async def admin_start(message: types.Message):
        if str(message.from_user.id) == ADMINS:
            res = session.query(User.id).all()
            for i in res:
                try:
                    text = (f"{get_name(session.query(User).filter(User.id == i[0]).first().flask)}, привет!"
                            f" Зайдите на сайт, чтобы продолжить выполнять задания и не сбивать свой прогресс.")
                    await bot.send_message(chat_id=i[0], text=text)
                except Exception as e:
                    print(e)
            await message.answer('Рассылка окончена!')
        else:
            await message.answer('Вы не админ!!!')
