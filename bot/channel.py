from config import CHANNEL_ID


async def publish(application, city, count):

    text = (
        f"🔴 <b>{city}</b>\n\n"
        f"Нет света\n\n"
        f"👥 Подтвердили: {count}"
    )

    await application.bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        parse_mode="HTML"
    )
