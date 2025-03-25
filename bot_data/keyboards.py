from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💬 Консультация")],
        [KeyboardButton(text="🌸 Заказать букет под желание")],
        [KeyboardButton(text="📷 Посмотреть коллекцию")],
    ],
    resize_keyboard=True
)
