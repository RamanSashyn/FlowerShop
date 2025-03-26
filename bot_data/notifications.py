from config import FLORIST_GROUP_ID
from aiogram import Bot, types


async def send_consultation_to_florist(bot: Bot, user: types.User, phone_number: str):
    """Отправляет контакт клиента во флорист-группу."""
    try:
        text = (
            f"🌸 *Новая заявка на консультацию!*\n\n"
            f"👤 Клиент: @{user.username or 'без username'} ({user.full_name})\n"
            f"📞 Телефон: {phone_number}"
        )
        await bot.send_message(FLORIST_GROUP_ID, text, parse_mode="Markdown")
    except Exception as e:
        print(f"[Ошибка уведомления флористам] {e}")
