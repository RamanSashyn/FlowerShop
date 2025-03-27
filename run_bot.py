import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerShop.settings')
django.setup()

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from dotenv import load_dotenv
from textwrap import dedent


load_dotenv()


from bot_data.handlers import register_handlers

bot = Bot(token=os.environ['TG_BOT_TOKEN'])
dispatcher = Dispatcher()


async def set_menu_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота")
    ])


async def main():

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
