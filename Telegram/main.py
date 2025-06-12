import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from Telegram.database.database import Session
from Telegram.database.constants import API_TOKEN
from Telegram.handlers.handlers import router, handlers
from Telegram.handlers.admin import router_for_admin, admin


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
session = Session()

if __name__ == '__main__':
    handlers(session)
    admin(session)

    dp.include_router(router)
    dp.include_router(router_for_admin)


    async def main():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


    asyncio.run(main())
