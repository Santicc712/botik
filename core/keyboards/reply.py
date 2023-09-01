from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_csv():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Экспорт БД')
    keyboard_builder.adjust(1, 2, 2)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True,
                                      input_field_placeholder='Экспорт')
