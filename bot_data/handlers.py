from aiogram import Bot, types, Dispatcher, F
from aiogram.filters import Command
from bot_data.keyboards import (
    get_start_keyboard,
    get_consultation_keyboard,
    get_theme_bouquet
    )
from textwrap import dedent


async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Я бот цветочного магазина 💐\nВыберите, что вас интересует:",
        reply_markup=get_start_keyboard()
    )


async def consultation_handler(callback: types.CallbackQuery, bot: Bot):
    user = callback.from_user
    print(user)
    manager_chat_id = 1612767132  # Тут потом вписать id консультанта (пока указан мой)

    await callback.message.answer("Наш менеджер скоро свяжется с вами 💬")
    await callback.answer()

    user_info = dedent(f"""\
        Новая заявка на консультацию!
        Имя: {user.full_name}
        ID: {user.id}
        Username: @{user.username}
    """)

    await bot.send_message(
        chat_id=manager_chat_id,
        text=user_info,
        reply_markup=get_consultation_keyboard(user.id)
    )


async def order_bouquet(callback: types.CallbackQuery, bot: Bot):

    await callback.message.edit_text(
        "Выберите повод для букета:",
        reply_markup=get_theme_bouquet()
    )
    await callback.answer()


# Для работы этой функции нужна модель букетов
# async def view_collection(callback: types.CallbackQuery, start_index: int = 0):
#     first_bouquet = bouquets[start_index]

#     bouquet = dedent(f"""
#     Название: {bouquet.name}
#     Состав: {bouquet.flowers}
#     Описание: {bouquet.description}
#     Цена: {bouquet.price} руб.
#     """)

#     await callback.message.answer_photo(
#         photo=bouquet.image_url,
#         caption=caption,
#         reply_markup=get_bouquet_keyboard(
#             current_index=start_index + 1,
#             total=len(bouquets)
#         )
#     )
#     await callback.answer()


# async def pagination_bouquets(callback: types.CallbackQuery):
#     action, bouquet_id = callback.data.split("_")
#     current_index = int(bouquet_id) - 1

#     if action == "prev" and current_index > 0:
#         new_index = current_index - 1
#     elif action == "next" and current_index < len(bouquets) - 1:
#         new_index = current_index + 1
#     else:
#         await callback.answer()
#         return

#     await callback.message.delete()
#     await view_collection(callback.message, bouquets[new_index], new_index)
#     await callback.answer()


def register_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command("start"))

    dp.callback_query.register(consultation_handler, F.data == "consultation")
    # dp.callback_query.register(view_collection, F.data == "view_collection")
    dp.callback_query.register(order_bouquet, F.data == "order_bouquet")

