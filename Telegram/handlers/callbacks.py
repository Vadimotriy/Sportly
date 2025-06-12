from aiogram import types, F, Router, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from Telegram.database.constants import *

router_for_callbacks = Router()

def callbacks(session):
    @router_for_callbacks.callback_query(F.data.startswith('*'))
    async def callback_query(callback_query: CallbackQuery, state: FSMContext):
        await callback_query.message.answer(text='Введите email, к которой привязан аккаунт Sportly:')
        await state.set_state(Logging.email)
        await callback_query.message.delete()
        await callback_query.answer()


