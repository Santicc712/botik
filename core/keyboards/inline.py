from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def get_garage_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Гараж', callback_data='list_cars')
    keyboard_builder.button(text='Добавить авто', callback_data='add_car')
    keyboard_builder.adjust(2, 1, 1)
    return keyboard_builder.as_markup()


def get_car_keyboard(cars) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    for car in cars:
        keyboard_builder.button(text=f'{car[1]} {car[2]}', callback_data=f'select_car:{car[0]}')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_selected_car_keyboard(car_id: int) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Редактировать название', callback_data=f'edit_car:{car_id}')
    keyboard_builder.button(text='Удалить авто', callback_data=f'delete_car:{car_id}')
    keyboard_builder.button(text='Ремонт', callback_data=f'repair_car:{car_id}')
    keyboard_builder.button(text='Хотелки', callback_data=f'wishlist_car:{car_id}')
    keyboard_builder.button(text='Найти информацию', callback_data='find_info')
    keyboard_builder.button(text='Назад', callback_data='list_cars')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_repair_keyboard(car_id: int) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Добавить запись', callback_data=f'add_repair:{car_id}')
    keyboard_builder.button(text='Список ремонтов', callback_data=f'list_repairs:{car_id}')
    keyboard_builder.button(text='Назад', callback_data=f'select_car:{car_id}')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_repair_action_keyboard(repair_id: int) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Редактировать', callback_data=f'edit_repair:{repair_id}')
    keyboard_builder.button(text='Удалить', callback_data=f'delete_repair:{repair_id}')
    keyboard_builder.button(text='Назад', callback_data=f'list_repairs:{repair_id}')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_wishlist_keyboard(car_id: int) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Добавить запись', callback_data=f'add_wishlist:{car_id}')
    keyboard_builder.button(text='Список хотелок', callback_data=f'list_wishlist:{car_id}')
    keyboard_builder.button(text='Назад', callback_data=f'select_car:{car_id}')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_wishlist_action_keyboard(wishlist_id: int) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Редактировать', callback_data=f'edit_wishlist:{wishlist_id}')
    keyboard_builder.button(text='Удалить', callback_data=f'delete_wishlist:{wishlist_id}')
    keyboard_builder.button(text='Назад', callback_data=f'list_wishlist:{wishlist_id}')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_back_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Назад', callback_data='list_cars')
    return keyboard_builder.as_markup()
