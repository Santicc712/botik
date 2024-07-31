from dotenv import load_dotenv
from MyProj.database import add_car, list_cars, add_repair, list_repairs, update_car, delete_car, \
    delete_repair, list_wishlist, add_wishlist, update_repair, delete_wishlist, update_wishlist
from aiogram import types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from MyProj.core.keyboards.inline import get_garage_keyboard, get_car_keyboard, get_selected_car_keyboard, \
    get_wishlist_action_keyboard, get_repair_action_keyboard, get_back_keyboard
from MyProj.core.keyboards.inline import get_repair_keyboard, get_wishlist_keyboard
import aiohttp
import os


# Обработчик для callback-запросов

class SearchStates(StatesGroup):
    waiting_for_query = State()


class AddCarStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_model = State()


class EditCarStates(StatesGroup):
    waiting_for_new_name = State()
    waiting_for_new_model = State()


class AddRepairStates(StatesGroup):
    waiting_for_description = State()
    waiting_for_date = State()


class EditRepairStates(StatesGroup):
    waiting_for_new_description = State()
    waiting_for_new_date = State()


class ChooseRepairStates(StatesGroup):
    waiting_for_number = State()


class ChooseWishStates(StatesGroup):
    waiting_for_number = State()


class AddWishlistStates(StatesGroup):
    waiting_for_description = State()


class EditWishlistStates(StatesGroup):
    waiting_for_new_description = State()


async def callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if callback_query.data == 'find_info':
        await callback_query.message.answer("Введите ваш запрос:")
        await state.set_state(SearchStates.waiting_for_query)

    elif callback_query.data == 'list_cars':
        cars = await list_cars(user_id)
        if cars:
            await callback_query.message.answer("Выберите машину:", reply_markup=get_car_keyboard(cars))
        else:
            await callback_query.message.answer("Нет добавленных машин.", reply_markup=get_garage_keyboard())
    elif callback_query.data == 'add_car':
        await callback_query.message.answer("Введите название авто:")
        await state.update_data(user_id=user_id)
        await state.set_state(AddCarStates.waiting_for_name)
    elif callback_query.data.startswith('select_car:'):
        car_id = int(callback_query.data.split(':')[1])
        await state.update_data(car_id=car_id)
        await callback_query.message.answer("Вы выбрали автомобиль. Выберите действие:",
                                            reply_markup=get_selected_car_keyboard(car_id))
    elif callback_query.data.startswith('edit_car:'):
        car_id = int(callback_query.data.split(':')[1])
        await state.update_data(car_id=car_id)
        await callback_query.message.answer("Введите новое название авто:")
        await state.set_state(EditCarStates.waiting_for_new_name)
    elif callback_query.data.startswith('delete_car:'):
        car_id = int(callback_query.data.split(':')[1])
        await delete_car(car_id)
        await callback_query.message.answer("Автомобиль удален.")
        cars = await list_cars(user_id)
        await callback_query.message.answer("Выберите машину:", reply_markup=get_car_keyboard(cars))
    elif callback_query.data.startswith('repair_car:'):
        car_id = int(callback_query.data.split(':')[1])
        await callback_query.message.answer("Выберите действие:", reply_markup=get_repair_keyboard(car_id))
    elif callback_query.data.startswith('add_repair:'):
        car_id = int(callback_query.data.split(':')[1])
        await state.update_data(car_id=car_id)
        await callback_query.message.answer("Введите описание ремонта:")
        await state.set_state(AddRepairStates.waiting_for_description)

    elif callback_query.data.startswith('list_repairs:'):
        car_id = int(callback_query.data.split(':')[1])
        repairs = await list_repairs(car_id)
        if repairs:
            await state.update_data(car_id=car_id, repairs=repairs)
            reply_message = "Список ремонтов:\n"
            for i, repair in enumerate(repairs, start=1):
                reply_message += f"{i}. {repair[1]} (Дата/Пробег: {repair[2]})\n"
            await callback_query.message.answer(reply_message, reply_markup=get_back_keyboard())
            await state.set_state(ChooseRepairStates.waiting_for_number)
        else:
            await callback_query.message.answer("Пока нет записей о ремонтах.")

    elif callback_query.data.startswith('edit_repair:'):
        repair_id = int(callback_query.data.split(':')[1])
        await state.update_data(repair_id=repair_id)
        await callback_query.message.answer("Введите новое описание ремонта:")
        await state.set_state(EditRepairStates.waiting_for_new_description)

    elif callback_query.data.startswith('delete_repair:'):
        repair_id = int(callback_query.data.split(':')[1])
        await delete_repair(repair_id)
        await callback_query.message.answer("Запись о ремонте удалена.")
        car_id = (await state.get_data())['car_id']
        repairs = await list_repairs(car_id)
        if repairs:
            await state.update_data(car_id=car_id)
            reply_message = "Список ремонтов:\n"
            for i, repair in enumerate(repairs, start=1):
                reply_message += f"{i}. {repair[1]} (Дата/Пробег: {repair[2]})\n"
            await callback_query.message.answer(reply_message, reply_markup=get_back_keyboard())
        else:
            await callback_query.message.answer("Пока нет записей о ремонтах.")

    elif callback_query.data.startswith('wishlist_car:'):
        car_id = int(callback_query.data.split(':')[1])
        await callback_query.message.answer("Выберите действие:", reply_markup=get_wishlist_keyboard(car_id))
    elif callback_query.data.startswith('add_wishlist:'):
        car_id = int(callback_query.data.split(':')[1])
        await state.update_data(car_id=car_id)
        await callback_query.message.answer("Введите описание хотелки:")
        await state.set_state(AddWishlistStates.waiting_for_description)
    elif callback_query.data.startswith('list_wishlist:'):
        car_id = int(callback_query.data.split(':')[1])
        wishlist = await list_wishlist(car_id)
        if wishlist:
            await state.update_data(car_id=car_id, wishlist=wishlist)
            reply_message = "Список хотелок:\n"
            for i, item in enumerate(wishlist, start=1):
                reply_message += f"{i}. {item[1]}\n"
            await callback_query.message.answer(reply_message, reply_markup=get_back_keyboard())
            await state.set_state(ChooseWishStates.waiting_for_number)
        else:
            await callback_query.message.answer("Пока нет записей о хотелках.")
    elif callback_query.data.startswith('edit_wishlist:'):
        wishlist_id = int(callback_query.data.split(':')[1])
        await state.update_data(wishlist_id=wishlist_id)
        await callback_query.message.answer("Введите новое описание хотелки:")
        await state.set_state(EditWishlistStates.waiting_for_new_description)
    elif callback_query.data.startswith('delete_wishlist:'):
        wishlist_id = int(callback_query.data.split(':')[1])
        await delete_wishlist(wishlist_id)
        await callback_query.message.answer("Запись о хотелке удалена.")
        car_id = (await state.get_data())['car_id']
        wishlist = await list_wishlist(car_id)
        if wishlist:
            await state.update_data(car_id=car_id)
            reply_message = ("Список хотелок:\n"
                             )
            for i, item in enumerate(wishlist, start=1):
                reply_message += f"{i}. {item[1]}\n"
                await callback_query.message.answer(reply_message, reply_markup=get_back_keyboard())
        else:
            await callback_query.message.answer("Пока нет записей о хотелках.")

    await callback_query.answer()


async def car_name_received(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = user_data['user_id']
    await state.update_data(name=message.text)
    await message.answer("Введите модель авто:")
    await state.set_state(AddCarStates.waiting_for_model)


async def car_model_received(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = user_data['user_id']
    car_name = user_data['name']
    car_model = message.text

    await add_car(user_id, car_name, car_model)
    await message.answer(f"Машина добавлена: {car_name} {car_model}")
    await state.clear()


async def new_car_name_received(message: types.Message, state: FSMContext):
    await state.update_data(new_name=message.text)
    await message.answer("Введите новую модель авто:")
    await state.set_state(EditCarStates.waiting_for_new_model)


async def new_car_model_received(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    car_id = user_data['car_id']
    new_name = user_data['new_name']
    new_model = message.text

    await update_car(car_id, new_name, new_model)
    await message.answer(f"Машина обновлена: {new_name} {new_model}")
    await state.clear()


async def repair_description_received(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите Дату/Пробег ремонта:")
    await state.set_state(AddRepairStates.waiting_for_date)


async def repair_date_received(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    car_id = user_data['car_id']
    description = user_data['description']
    date = message.text

    await add_repair(car_id, description, date)
    await message.answer("Запись о ремонте добавлена.")
    await state.clear()


async def new_repair_description_received(message: types.Message, state: FSMContext):
    await state.update_data(new_description=message.text)
    await message.answer("Введите новую дату ремонта :")
    await state.set_state(EditRepairStates.waiting_for_new_date)


async def new_repair_date_received(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    repair_id = user_data['repair_id']
    new_description = user_data['new_description']
    new_date = message.text

    await update_repair(repair_id, new_description, new_date)
    await message.answer("Запись о ремонте обновлена.")
    await state.clear()


async def wishlist_description_received(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    car_id = user_data['car_id']
    description = message.text

    await add_wishlist(car_id, description)
    await message.answer("Запись о хотелке добавлена.")
    await state.clear()


async def new_wishlist_description_received(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    wishlist_id = user_data['wishlist_id']
    new_description = message.text

    await update_wishlist(wishlist_id, new_description)
    await message.answer("Запись о хотелке обновлена.")
    await state.clear()


async def repair_selection_handler(message: types.Message, state: FSMContext):
    try:
        repair_index = int(message.text) - 1
        data = await state.get_data()
        user_data = await state.get_data()
        car_id = user_data['car_id']
        repairs = data.get('repairs', [])
        if 0 <= repair_index < len(repairs):
            selected_repair = repairs[repair_index]
            await state.update_data(selected_repair_id=selected_repair[0])
            await message.answer(
                f"Выбранный ремонт:\nОписание: {selected_repair[1]}\nДата/Пробег: {selected_repair[2]}",
                reply_markup=get_repair_action_keyboard(selected_repair[0])
            )
            await state.set_state(ChooseRepairStates.waiting_for_number)
        else:
            await message.answer("Неверный номер ремонта.")
    except ValueError:
        await message.answer("Пожалуйста, введите номер ремонта.")


async def wishlist_selection_handler(message: types.Message, state: FSMContext):
    try:
        wishlist_index = int(message.text) - 1
        data = await state.get_data()
        user_data = await state.get_data()
        car_id = user_data['car_id']
        wishlist = data.get('wishlist', [])
        if 0 <= wishlist_index < len(wishlist):
            selected_item = wishlist[wishlist_index]
            await state.update_data(selected_wishlist_id=selected_item[0])
            await message.answer(
                f"Выбранная хотелка:\n{selected_item[1]}",
                reply_markup=get_wishlist_action_keyboard(selected_item[0])
            )
            await state.set_state(ChooseWishStates.waiting_for_number)
        else:
            await message.answer("Неверный номер хотелки.")
    except ValueError:
        await message.answer("Пожалуйста, введите номер хотелки.")


async def handle_query(message: types.Message, state: FSMContext):
    query = message.text
    await state.clear()
    results = await search_information(query)
    await message.answer(results)

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CX = os.getenv('GOOGLE_CX')


async def search_information(query: str) -> str:
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CX,
        'q': query,
        'num': 5  # Количество результатов, которые хотите получить
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                items = data.get('items', [])
                results = [f"{i+1}. {item['title']} - {item['link']}" for i, item in enumerate(items)]
                return "\n".join(results)
            else:
                return "Произошла ошибка при получении результатов поиска."