import asyncio
from aiogram import Bot, Dispatcher
from bot_data.handlers import register_handlers


BOT_TOKEN = "7946435543:AAEkCNi2cyx6bD7lcPFdZWHzj6wthYQarcM"

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    register_handlers(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

