from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💬 Консультация", 
            callback_data="consultation"
        )],
        [InlineKeyboardButton(
            text="📷 Посмотреть коллекцию",
            callback_data="view_collection"
        )],
        [InlineKeyboardButton(
            text="🌸 Заказать букет под желание",
            callback_data="order_bouquet"
        )],
    ])


def get_preferred_option():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📞 По телефону", 
            callback_data="by_phone"
        )],
        [InlineKeyboardButton(
            text="💬 В чате",
            callback_data="in_chat"
        )]
    ])


def get_phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="Отправить номер телефона",
                request_contact=True
            )]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_consultation_keyboard(user_id):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="📨 Ответить",
        url=f"tg://user?id={user_id}"
    )
    return builder.as_markup()


def get_theme_bouquet():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🎂 День рождения",
            callback_data="birthday"
        ),
        types.InlineKeyboardButton(
            text="💍 Свадьба",
            callback_data="wedding"
        )
    )
    builder.row(
        types.InlineKeyboardButton(text="🏫 В школу", callback_data="school"),
        types.InlineKeyboardButton(
            text="🌹 Без повода",
            callback_data="no_reson"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="✏️ Другой повод",
            callback_data="custom"
        )
    )
    return builder.as_markup()


def get_bouquet_keyboard(current_index: int, total: int, bouquet_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="◀️ Назад",
        callback_data=f"prev_{current_index}"
    )

    builder.button(text="🛒 Заказать", callback_data=f"order_{bouquet_id}")

    builder.button(
        text="Вперед ▶️",
        callback_data=f"next_{current_index}"
    )

    builder.adjust(3)
    return builder.as_markup()


def get_price_keyboards():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="~500 руб.",
            callback_data="500"
        ),
        types.InlineKeyboardButton(
            text="~1000 руб.",
            callback_data="1000"
        )
    )
    builder.row(
        types.InlineKeyboardButton(text="~2000 руб.", callback_data="2000"),
        types.InlineKeyboardButton(
            text="Больше.",
            callback_data="more"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Не важно",
            callback_data="no_matter"
        )
    )
    return builder.as_markup()
