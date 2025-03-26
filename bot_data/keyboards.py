from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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