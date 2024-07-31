from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начать'
        )
        ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def set_admin(bot: Bot):
    commands = [
        BotCommand(
            command='admin',
            description='Админ'
        ),
        BotCommand(
            command='start',
            description='Начать'
        )
        ]
    await bot.set_my_commands(commands, BotCommandScopeChat(chat_id=400299512))
