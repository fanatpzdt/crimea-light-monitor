from config import CHANNEL_ID


async def publish(application, city, count):

    text = (
        "🚨 Возможное отключение электроэнергии\n\n"
        f"📍 {city}\n\n"
        f"Подтвердили: {count} человек"
    )

    await application.bot.send_message(
        chat_id=CHANNEL_ID,
        text=text
    )
