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


@dispatcher.message(Command("start"))
async def start(message: types.Message):
    await message.answer(dedent("""\
                Закажите доставку праздничного букета 💐
                собранного специально для ваших любимых,
                родных и коллег ❤️.
                Наш букет со смыслом станет главным
                подарком на вашем празднике 😊
    """))
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Консультация", callback_data="btn1")],
        [InlineKeyboardButton(
            text="Посмотреть коллекцию",
            callback_data="btn2"
        )],
        [InlineKeyboardButton(
            text="Заказать букет под желание",
            callback_data="btn2"
        )],
    ])
    await message.answer("Выберите действие:", reply_markup=inline_kb)


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
