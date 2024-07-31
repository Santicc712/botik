import os
import asyncpg
from datetime import datetime
from _csv import writer
from aiogram.types import Message
from MyProj.core.keyboards.reply import get_csv
from aiogram.types import FSInputFile
from aiogram import Bot

LIST_ADMINS = [400299512]
CSV_FILE = 'Python_bot'
LIST_SUBJECTS = ["user_id", "first_name", "last_name", "username"]


async def get_admin(message: Message):
    if message.from_user.id in LIST_ADMINS:
        await message.answer('Вы в панели Admin.', reply_markup=get_csv())
    else:
        await message.answer(f'У вас нет доступа к панели Admin!')


async def run_db_export(message: Message, bot: Bot):
    admin_here = message.from_user.id
    zzz = await db_export()

    date_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    date_time_2 = str(date_time)
    csv_here = CSV_FILE + date_time_2 + '.csv'

    with open(csv_here, mode='a', encoding='utf-8', newline='') as file:
        writer_object = writer(file)
        writer_object.writerow(LIST_SUBJECTS)
        writer_object.writerows(zzz)
        file.close()

    await bot.send_document(admin_here, FSInputFile(f"{csv_here}"))

    os.remove(csv_here)


async def db_export():
    connection = await asyncpg.connect(host="127.0.0.1", user="santr", password="qwer4455", database="Garage_bot")

    try:
        async with connection.transaction():
            query = "SELECT * FROM user_pro ORDER BY user_id DESC"
            result = await connection.fetch(query)
            return result
    finally:
        await connection.close()
