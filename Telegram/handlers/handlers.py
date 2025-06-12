from aiogram import types, F, Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from Telegram.database.constants import *
from Telegram.database.functions import make_keyboard, make_keyboard_inline
from Telegram.database.database import User, Session
from Telegram.flask_api.flask_api import *

router = Router()


def handlers(session: Session):
    @router.message(Logging.password, F.text)
    async def email(message: types.Message, state: FSMContext):
        try:
            password = message.text
            email = await state.get_data()
            email = email['email']

            res = check_password(email, password)
            if res:
                user = session.query(User).filter(User.id == message.from_user.id).first()
                user.logged = True
                user.flask = res
                session.commit()

                name = get_name(str(res))
                await message.answer(text=f'Вы вошли в аккаунт {name}.')
                await state.clear()
            else:
                await message.answer(text='Неверный пароль. Повторите попытку:')
        except Exception as e:
            print(e)
            await message.answer(text='Введите корректный пароль!')

    @router.message(Logging.password)
    async def chooser_incorrectly(message: types.Message):
        await message.answer(text="Введите пароль!")

    @router.message(Logging.email, F.text)
    async def email(message: types.Message, state: FSMContext):
        try:
            email = message.text
            if checkemail(email):
                await message.answer(text='Введите пароль:')
                await state.update_data(email=email)
                await state.set_state(Logging.password)
            else:
                await message.answer(text='Пользователя с этим email не существует. Повторите попытку:',
                                     reply_markup=make_keyboard())
        except Exception as e:
            print(e)
            await message.answer(text='Введите корректный email!')

    @router.message(Logging.email)
    async def chooser_incorrectly(message: types.Message):
        await message.answer(text="Введите email!")

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
            text = start_message_logged + str(get_name(res.flask)) + '.'
            if str(message.from_user.id) == ADMINS:
                keyboard = make_keyboard(BUTTONS['buttons'] + ADMIN_BTN, adjust=1)
            else:
                keyboard = make_keyboard()
            await message.answer(text=text, reply_markup=keyboard)

    @router.message(F.text == 'Выйти')
    async def logout(message: types.Message):
        user = session.query(User).filter(User.id == message.from_user.id).first()
        user.logged = False
        user.flask = None
        keyboard = make_keyboard_inline(['Войти'], 1, message.from_user.id)
        await message.answer(text='Вы вышли с аккаунта.', reply_markup=keyboard)
        session.commit()

    @router.message(F.text == 'Выйти')
    async def logout(message: types.Message):
        user = session.query(User).filter(User.id == message.from_user.id).first()
        user.logged = False
        user.flask = None
        keyboard = make_keyboard_inline(['Войти'], 1, message.from_user.id)
        await message.answer(text='Вы вышли с аккаунта.', reply_markup=keyboard)
        session.commit()

    @router.message(F.text == '')