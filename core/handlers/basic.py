from aiogram import Bot
from aiogram.types import Message
from MyProj.core.utils.commands import set_admin
from MyProj.core.keyboards.inline import get_garage_keyboard


async def get_start(message: Message, bot: Bot):
    if message.from_user.id == 400299512:
        await set_admin(bot)
    await message.answer(f'Привет. Я Гараж-бот,помогу следить за твоим авто.', reply_markup=get_garage_keyboard())


