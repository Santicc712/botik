from aiogram import Bot
from aiogram.types import Message
from core.utils.dbconnect import Request
from core.utils.commands import set_admin


async def get_start(message: Message, request: Request, bot: Bot):
    if message.from_user.id == 293037127:
        await set_admin(bot)
    await request.add_user(user_id=message.from_user.id,
                           first_name=message.from_user.first_name,
                           last_name=message.from_user.last_name,
                           username=message.from_user.username)
    await message.answer(f'Привет. Я бот созданный @ITsmiths.')

