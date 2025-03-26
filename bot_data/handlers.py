from aiogram import types, Dispatcher, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot_data.keyboards import main_menu_kb
from bot_data.notifications import send_consultation_to_florist


class ConsultationStates(StatesGroup):
    waiting_for_phone = State()


async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Я бот цветочного магазина 💐\nВыберите, что вас интересует:",
        reply_markup=main_menu_kb
    )

async def message_handler(message: types.Message, state: FSMContext):
    text = message.text

    if text == "💬 Консультация":
        await message.answer("Укажите номер телефона, и наш флорист перезвонит вам в течение 20 минут 📞")
        await state.set_state(ConsultationStates.waiting_for_phone)

    elif text == "🌸 Заказать букет под желание":
        await message.answer("Расскажите, какой букет вы хотите 🌷")

    elif text == "📷 Посмотреть коллекцию":
        await message.answer("Вот наша коллекция: [ссылка или фото] 📸")

    else:
        await message.answer("Пожалуйста, выберите один из пунктов меню.")


async def phone_input_handler(message: types.Message, state: FSMContext, bot: Bot):
    user = message.from_user
    phone = message.text.strip()

    # Сообщение пользователю
    await message.answer(
        "Флорист скоро свяжется с вами. А пока можете присмотреть что-нибудь из готовой коллекции 📸"
    )

    await message.answer_photo(
        photo="https://images.app.goo.gl/UFR1SwyMezC35GrF6",  # пример фото
        caption="💐 Букет «Нежность» — 2000₽",
        reply_markup=main_menu_kb
    )

    # Уведомление в группу
    await send_consultation_to_florist(bot, user, phone)

    await state.clear()


def register_handlers(dp: Dispatcher):
    dp.message.register(phone_input_handler, ConsultationStates.waiting_for_phone)
    dp.message.register(start_handler, F.text == "/start")
    dp.message.register(message_handler, F.text)
