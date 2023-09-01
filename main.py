import logging
import sys
import contextlib
import asyncio
import asyncpg
from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import CommandStart, Command
from core.settings import settings
from core.handlers.basic import get_start
from core.utils.commands import set_commands
from core.middlewares.Dbmiddleware import DbSession
from core.handlers.admin import get_admin, run_db_export


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='START')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='STOP')


async def create_pool():
    return await asyncpg.create_pool(user=settings.db.db_user, password=settings.db.dp_password,
                                     database=settings.db.db_database, host=settings.db.db_host,
                                     port=5432, command_timeout=60)


async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    bot: Bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    pool_connect = await create_pool()
    dp: Dispatcher = Dispatcher()
    dp.update.middleware.register(DbSession(pool_connect))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_start, CommandStart())
    dp.message.register(get_admin, Command(commands='admin'))
    dp.message.register(run_db_export, F.text == 'Экспорт БД')

    try:
        await dp.start_polling(bot)
    except Exception as ex:
        logging.error(f"[!!! Exception] - {ex}", exc_info=True)
    finally:
        await bot.session.close()

if __name__ == '__main__':

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())
