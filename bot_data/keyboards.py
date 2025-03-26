from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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