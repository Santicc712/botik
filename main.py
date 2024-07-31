import logging
import sys
import contextlib
import asyncio
from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import CommandStart, Command
from core.settings import settings
from core.handlers.basic import get_start
from core.handlers.allcmnd import add_car, add_repair, list_cars, list_repairs, \
    AddCarStates, new_car_name_received, new_car_model_received, EditCarStates, repair_description_received, \
    AddRepairStates, repair_date_received, wishlist_description_received, AddWishlistStates, \
    new_repair_description_received, EditRepairStates, new_repair_date_received, new_wishlist_description_received, \
    EditWishlistStates, repair_selection_handler, ChooseRepairStates, ChooseWishStates, wishlist_selection_handler, \
    handle_query, SearchStates
from core.utils.commands import set_commands
from core.handlers.admin import get_admin, run_db_export
from core.handlers.allcmnd import callback_handler, car_name_received, car_model_received
from MyProj.database import init_db
from aiogram.fsm.storage.memory import MemoryStorage


async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    bot: Bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()
    dp.message.register(get_start, CommandStart())
    dp.message(Command("list_cars"))(list_cars)
    dp.message(Command("add_repair"))(add_repair)
    dp.message(Command("list_repairs"))(list_repairs)
    dp.callback_query.register(callback_handler)
    dp.message.register(car_name_received, AddCarStates.waiting_for_name)
    dp.message.register(car_model_received, AddCarStates.waiting_for_model)
    dp.message.register(new_car_name_received, EditCarStates.waiting_for_new_name)
    dp.message.register(new_car_model_received, EditCarStates.waiting_for_new_model)
    dp.message.register(repair_description_received, AddRepairStates.waiting_for_description)
    dp.message.register(repair_date_received, AddRepairStates.waiting_for_date)
    dp.message.register(new_repair_description_received, EditRepairStates.waiting_for_new_description)
    dp.message.register(new_repair_date_received, EditRepairStates.waiting_for_new_date)
    dp.message.register(wishlist_description_received, AddWishlistStates.waiting_for_description)
    dp.message.register(new_wishlist_description_received, EditWishlistStates.waiting_for_new_description)
    dp.message.register(repair_selection_handler, ChooseRepairStates.waiting_for_number)
    dp.message.register(wishlist_selection_handler, ChooseWishStates.waiting_for_number)
    dp.message.register(handle_query, SearchStates.waiting_for_query)
    dp.message.register(get_admin, Command(commands='admin'))
    dp.message.register(run_db_export, F.text == 'Экспорт БД')

    try:
        await init_db()  # Инициализация базы данных
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
