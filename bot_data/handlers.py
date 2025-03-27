from aiogram import Bot, types, Dispatcher, F
from aiogram.filters import Command
from bot_admin.models import ConsultationRequest
from bot_data.keyboards import (
    get_start_keyboard,
    get_consultation_keyboard,
    get_theme_bouquet,
    get_preferred_option,
    get_phone_keyboard,
    get_bouquet_keyboard,
    )
from textwrap import dedent
from bot_admin.models import Bouquet


async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Я бот цветочного магазина 💐\nВыберите, что вас интересует:",
        reply_markup=get_start_keyboard()
    )


async def consultation_handler(callback: types.CallbackQuery, bot: Bot):
    await callback.message.edit_text(
        "Выберите предпочитаемый вариант связи с нашим менеджером",
        reply_markup=get_preferred_option()
    )


async def notify_manager(bot: Bot, user: types.User, contact_method: str, phone_number: str = None):
    manager_chat_id = -4743309026

    message_text = dedent(f"""\
        Новая заявка на консультацию!
        Имя: {user.full_name}
        ID: {user.id}
        Username: @{user.username}
        Способ связи: {contact_method}
    """)

    if phone_number:
        message_text += f"\nНомер телефона: {phone_number}"

    await bot.send_message(
        chat_id=manager_chat_id,
        text=message_text,
        reply_markup=get_consultation_keyboard(user.id)
    )


async def contact_option(callback: types.CallbackQuery, bot: Bot):
    user = callback.from_user

    if callback.data == "in_chat":

        await ConsultationRequest.objects.acreate(
            full_name=user.full_name,
            telegram_username=user.username,
            phone_number="— через чат —"
        )

        await notify_manager(bot, user, "💬 Чат")
        await callback.message.answer("Наш менеджер скоро свяжется с вами в чате 💬")

    elif callback.data == "by_phone":
        await callback.message.answer(
            "Для отправки номера телефона нажмите кнопку снизу ⬇️",
            reply_markup=get_phone_keyboard()
        )

    await callback.answer()


async def handle_contact(message: types.Message, bot: Bot):
    if message.contact:

        await ConsultationRequest.objects.acreate(
            full_name=message.from_user.full_name,
            telegram_username=message.from_user.username,
            phone_number=message.contact.phone_number,
        )

        await notify_manager(
            bot=bot,
            user=message.from_user,
            contact_method="📞 Телефон",
            phone_number=message.contact.phone_number
        )
        await message.answer(
            dedent("""\
            Спасибо! Менеджер свяжется с вами по указанному номеру,
            в течение 20 минут.
            """),
            reply_markup=types.ReplyKeyboardRemove()
        )


async def order_bouquet(callback: types.CallbackQuery, bot: Bot):

    await callback.message.edit_text(
        "Выберите повод для букета:",
        reply_markup=get_theme_bouquet()
    )
    await callback.answer()


async def view_collection(callback: types.CallbackQuery, start_index: int = 0):
    bouquets = [b async for b in Bouquet.objects.all()]
    current_bouquet = bouquets[start_index]

    caption = dedent(f"""
    Название: {current_bouquet.name}
    Состав: {current_bouquet.flowers}
    Описание: {current_bouquet.description}
    Цена: {current_bouquet.price} руб.
    """)

    image_url = types.FSInputFile(current_bouquet.image.path)

    await callback.message.answer_photo(
        photo=image_url,
        caption=caption,
        reply_markup=get_bouquet_keyboard(
            current_index=start_index + 1,
            total=len(bouquets)
        )
    )
    await callback.answer()


async def pagination_bouquets(callback: types.CallbackQuery):
    action, bouquet_id = callback.data.split("_")
    current_index = int(bouquet_id)
    total = await Bouquet.objects.acount()

    if action == "prev":
        new_index = current_index - 1 if current_index > 1 else total
    elif action == "next":
        new_index = current_index + 1 if current_index < total else 1

    await callback.message.delete()
    await view_collection(callback, new_index - 1)
    await callback.answer()


async def get_price(callback: types.CallbackQuery, bot: Bot):
    await callback.message.edit_text(
        "На какую сумму рассчитываете?",
        reply_markup=get_theme_bouquet()
    )
    await callback.answer()


def register_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command("start"))

    dp.callback_query.register(consultation_handler, F.data == "consultation")
    dp.message.register(handle_contact, F.contact)
    dp.callback_query.register(contact_option, F.data.in_([
        "in_chat",
        "by_phone"
    ]))
    dp.callback_query.register(view_collection, F.data == "view_collection")
    dp.callback_query.register(order_bouquet, F.data == "order_bouquet")
    dp.callback_query.register(get_price, F.data.in_([
        "birthday",
        "wedding",
        "school",
        "no_reson",
        "custom"
    ]))
    dp.callback_query.register(pagination_bouquets, F.data.startswith("next_"))
    dp.callback_query.register(pagination_bouquets, F.data.startswith("prev_"))