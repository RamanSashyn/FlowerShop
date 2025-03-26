import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    BotCommand,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from bot_data.handlers import register_handlers
from dotenv import load_dotenv
from textwrap import dedent

bot = Bot(token=os.environ['TG_BOT_TOKEN'])
dispatcher = Dispatcher()


async def set_menu_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота")
    ])


async def main():
    load_dotenv()

    if not bot.token:
        print(dedent("""\
            Ошибка: Не указан TG_BOT_TOKEN.
            Убедитесь, что он задан в переменных окружения.
        """))
        return

    await set_menu_commands(bot)

    register_handlers(dispatcher)

    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот запущен!")
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
