from aiogram import types, Dispatcher, F
from bot_data.keyboards import main_menu_kb

async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Я бот цветочного магазина 💐\nВыберите, что вас интересует:",
        reply_markup=main_menu_kb
    )

async def message_handler(message: types.Message):
    text = message.text

    if text == "💬 Консультация":
        await message.answer("Наш менеджер скоро свяжется с вами 💬")
    elif text == "🌸 Заказать букет под желание":
        await message.answer("Расскажите, какой букет вы хотите 🌷")
    elif text == "📷 Посмотреть коллекцию":
        await message.answer("Вот наша коллекция: [ссылка или фото] 📸")
    else:
        await message.answer("Пожалуйста, выберите один из пунктов меню.")

def register_handlers(dp: Dispatcher):
    dp.message.register(start_handler, F.text == "/start")
    dp.message.register(message_handler, F.text)
