from datetime import datetime
from textwrap import dedent
import os

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from django.db.models import Q

from bot_admin.models import Bouquet, ConsultationRequest, Order
from bot_data.keyboards import (
    get_bouquet_keyboard,
    get_collection_keyboard,
    get_consultation_phone_keyboard,
    get_consultation_keyboard,
    get_order_phone_keyboard,
    get_preferred_option,
    get_price_keyboards,
    get_start_keyboard,
    get_theme_bouquet
)


router = Router()


class OrderStates(StatesGroup):
    GET_PHONE = State()
    GET_NAME = State()
    GET_ADDRESS = State()
    GET_DATE = State()
    GET_TIME = State()


async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Я бот цветочного магазина 💐\nВыберите, что вас интересует:",
        reply_markup=get_start_keyboard()
    )


async def show_consultation_options(callback: types.CallbackQuery):
    text = "Выберите предпочитаемый вариант связи с нашим менеджером"
    keyboard = get_preferred_option()
    if callback.message.text:
        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard,
        )

    elif callback.message.caption:
        await callback.message.edit_caption(
            caption=text,
            reply_markup=keyboard,
        )
    await callback.answer()


async def notify_manager(
        bot: Bot,
        user: types.User,
        contact_method: str,
        phone_number: str = None
):
    manager_chat_id = os.getenv("TG_CONSULTANT_CHAT_ID")
    if not manager_chat_id:
        print('Ошибка: Не указан чат-id коньсультанта.')
        return

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


async def handle_contact_preference(callback: types.CallbackQuery, bot: Bot):
    user = callback.from_user

    if callback.data == "in_chat":

        await ConsultationRequest.objects.acreate(
            full_name=user.full_name,
            telegram_username=user.username,
            phone_number="— через чат —"
        )

        await notify_manager(bot, user, "💬 Чат")
        await callback.message.answer(
            dedent("""\
            Наш менеджер скоро свяжется с вами в чате 💬
            А пока можете присмотреть что-нибудь из готовой коллекции
            """),
            reply_markup=get_collection_keyboard()
        )

    elif callback.data == "by_phone":
        await callback.message.answer(
            "Для отправки номера телефона нажмите кнопку снизу ⬇️",
            reply_markup=get_consultation_phone_keyboard()
        )

    await callback.answer()


async def get_phone(message: types.Message, bot: Bot, state: FSMContext):
    current_state = await state.get_state()
    if current_state == OrderStates.GET_PHONE.state:
        await process_phone(message, state, bot)
        return

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
            А пока можете присмотреть что-нибудь из готовой коллекции.
            """),
            reply_markup=get_collection_keyboard()
        )


async def show_bouquet_occasions(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выберите повод для букета:",
        reply_markup=get_theme_bouquet()
    )
    await callback.answer()


async def handle_price(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    if parts[1] == 'no' and parts[2] == 'matter':
        price = 'no_matter'
        occasion = "_".join(parts[3:]) if len(parts) > 3 else None
    else:
        price = parts[1]
        occasion = "_".join(parts[2:]) if len(parts) > 2 else None
    await show_filtered_bouquets(callback, occasion=occasion, price=price)


async def view_collection(
        callback: types.CallbackQuery,
        occasion: str = None,
        price: str = None,
        start_index: int = 0
):
    await show_filtered_bouquets(callback, occasion, price, start_index)
    await callback.answer()


async def filter_bouquets(query, occasion, price):
    if occasion and occasion != 'occasion_custom':
        query = query.filter(
            Q(occasion=occasion) | Q(occasion="occasion_custom")
        )

    elif occasion == "occasion_custom":
        query = query.filter(occasion="occasion_custom")

    if price is not None and price != 'no_matter':
        if price == "500":
            query = query.filter(price__lte=500)
        elif price == "1000":
            query = query.filter(price__lte=1000)
        elif price == "2000":
            query = query.filter(price__lte=2000)
        elif price == "more":
            query = query.filter(price__gt=2000)

    return query


async def show_filtered_bouquets(
        callback: types.CallbackQuery,
        occasion: str = None,
        price: str = None,
        start_index: int = 0,
):
    query = Bouquet.objects.all()
    query = await filter_bouquets(query, occasion, price)

    bouquets = [b async for b in query]

    if not bouquets:
        await callback.message.answer(
            dedent("""\
                Нет доступных букетов по заданным критериям.
                Попробуйте другие критерии или посмотрите всю коллекцию.
                Так же вы можете обратиться за помощью к нашему консультанту.
            """),
            reply_markup=get_start_keyboard()
        )
        return

    start_index = max(0, min(start_index, len(bouquets) - 1))
    current_bouquet = bouquets[start_index]

    caption = dedent(f"""
    <b>Название:</b> {current_bouquet.name}
    <b>Состав:</b> {current_bouquet.flowers}
    <b>Описание:</b> {current_bouquet.description}
    <b>Цена:</b> {current_bouquet.price} руб.

    <b>Хотите что-то еще более уникальное?
    Подберите другой букет из нашей коллекции или
    закажите консультацию флориста.</b>
    """)

    image_url = types.FSInputFile(current_bouquet.image.path)

    await callback.message.answer_photo(
        photo=image_url,
        caption=caption,
        parse_mode=ParseMode.HTML,
        reply_markup=get_bouquet_keyboard(
            bouquet_id=current_bouquet.id,
            current_index=start_index + 1,
            total=len(bouquets),
            occasion=occasion,
            price=price
        )
    )
    await callback.answer()


async def navigate_bouquet_catalog(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    action = parts[0]
    current_index = int(parts[1])

    price = None
    occasion = None

    if len(parts) > 2:
        if parts[2] == 'no' and len(parts) > 3 and parts[3] == 'matter':
            price = 'no_matter'
            occasion = "_".join(parts[4:]) if len(parts) > 4 else None
        else:
            price = parts[2]
            occasion = "_".join(parts[3:]) if len(parts) > 3 else None

    query = Bouquet.objects.all()

    query = await filter_bouquets(query, occasion, price)

    bouquets = [b async for b in query]
    total = len(bouquets)

    current_position = current_index - 1

    if action == "prev":
        new_position = (current_position - 1) % total
    elif action == "next":
        new_position = (current_position + 1) % total

    await callback.message.delete()
    await show_filtered_bouquets(
        callback,
        occasion=occasion,
        price=price,
        start_index=new_position
    )
    await callback.answer()


async def get_price(callback: types.CallbackQuery):
    occasion = callback.data.replace("occasion_", "")
    await callback.message.edit_text(
        "На какую сумму рассчитываете?",
        reply_markup=get_price_keyboards(occasion=occasion)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("order_"))
async def start_order_process(
    callback: types.CallbackQuery,
    state: FSMContext
):
    bouquet_id = int(callback.data.split("_")[1])
    bouquet = await Bouquet.objects.aget(id=bouquet_id)
    await state.update_data(
        bouquet_id=bouquet.id,
        bouquet_name=bouquet.name
    )
    await callback.message.answer("Пожалуйста, напишите ваше имя")
    await state.set_state(OrderStates.GET_NAME)
    await callback.answer()


@router.message(OrderStates.GET_NAME)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await message.answer("Пожалуйста, введите адрес доставки:")
    await state.set_state(OrderStates.GET_ADDRESS)


@router.message(OrderStates.GET_ADDRESS)
async def process_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Введите дату доставки (в формате ДД.ММ.ГГГГ):")
    await state.set_state(OrderStates.GET_DATE)


@router.message(OrderStates.GET_DATE)
async def process_date(message: types.Message, state: FSMContext):
    try:
        delivery_date = datetime.strptime(message.text, "%d.%m.%Y").date()
        if delivery_date < datetime.now().date():
            await message.answer(
                "Дата не может быть в прошлом. Введите корректную дату:"
            )
            return

        await state.update_data(delivery_date=delivery_date)
        await message.answer("Введите время доставки (в формате ЧЧ:ММ):")
        await state.set_state(OrderStates.GET_TIME)
    except ValueError:
        await message.answer(
            "Неверный формат даты. Введите дату в формате ДД.ММ.ГГГГ:"
        )


@router.message(OrderStates.GET_TIME)
async def process_time(message: types.Message, state: FSMContext):
    try:
        delivery_time = datetime.strptime(message.text, "%H:%M").time()
        await state.update_data(delivery_time=delivery_time)
        await message.answer(
            "Для оформления заказа нам нужен ваш номер телефона.\n"
            "Нажмите на кнопку ниже для передачи номера:",
            reply_markup=get_order_phone_keyboard()
        )
        await state.set_state(OrderStates.GET_PHONE)
    except ValueError:
        await message.answer(
            "Неверный формат времени. Введите время в формате ЧЧ:ММ:"
        )


@router.message(OrderStates.GET_PHONE, F.contact)
async def process_phone(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    bouquet = await Bouquet.objects.aget(id=data['bouquet_id'])
    order = await Order.objects.acreate(
        bouquet=bouquet,
        customer_name=data['client_name'],
        telegram_username=message.from_user.username,
        phone=message.contact.phone_number,
        address=data['address'],
        delivery_date=data['delivery_date'],
        delivery_time=data['delivery_time'],
        status="в обработке"
    )

    await send_order_confirmation(message, bouquet, data, order)
    await notify_courier_about_order(bot, bouquet, data, message, order)

    await state.clear()


async def send_order_confirmation(
    message: types.Message,
    bouquet: Bouquet,
    order_data: dict,
    order: Order
):
    confirmation_text = dedent(f"""\
        ✅ Ваш заказ успешно оформлен!
        Букет: {bouquet.name}
        Цена: {bouquet.price} руб.
        Имя: {order_data['client_name']}
        Адрес: {order_data['address']}
        Дата: {order_data['delivery_date'].strftime('%d.%m.%Y')}
        Время: {order_data['delivery_time'].strftime('%H:%M')}
        Телефон: {message.contact.phone_number}
        Номер заказа: {order.id}
    """)

    await message.answer(
        confirmation_text,
        reply_markup=types.ReplyKeyboardRemove()
    )


async def notify_courier_about_order(
    bot: Bot,
    bouquet: Bouquet,
    order_data: dict,
    message: types.Message,
    order: Order
):
    courier_chat_id = os.getenv("TG_COURIER_CHAT_ID")
    if not courier_chat_id:
        print('Ошибка: Не указан чат-id курьера.')
        return

    courier_message = dedent(f"""\
        НОВЫЙ ЗАКАЗ
        Букет: {bouquet.name}
        Цена: {bouquet.price} руб.
        Клиент: {order_data['client_name']} (@{message.from_user.username})
        Телефон: {message.contact.phone_number}
        Адрес: {order_data['address']}
        Дата: {order_data['delivery_date'].strftime('%d.%m.%Y')}
        Время: {order_data['delivery_time'].strftime('%H:%M')}
        Номер заказа: {order.id}
    """)

    await bot.send_message(
        chat_id=courier_chat_id,
        text=courier_message
    )


def register_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command("start"))

    dp.callback_query.register(
        show_consultation_options, F.data == "consultation"
    )
    dp.message.register(get_phone, F.contact)
    dp.callback_query.register(handle_contact_preference, F.data.in_([
        "in_chat",
        "by_phone"
    ]))
    dp.callback_query.register(view_collection, F.data == "view_collection")
    dp.callback_query.register(
        show_bouquet_occasions, F.data == "order_bouquet"
    )
    dp.callback_query.register(get_price, F.data.startswith("occasion_"))
    dp.callback_query.register(handle_price, F.data.startswith("price_"))
    dp.callback_query.register(
        navigate_bouquet_catalog, F.data.startswith("next_")
    )
    dp.callback_query.register(
        navigate_bouquet_catalog, F.data.startswith("prev_")
    )
    dp.callback_query.register(
        start_order_process, F.data.startswith("order_"))