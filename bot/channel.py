from config import CHANNEL_ID
from database import get_alert, save_alert


async def publish(application, city, count):

    message_id = get_alert(city)


    text = (
        f"🔴 <b>{city}</b>\n\n"
        f"Нет света\n\n"
        f"👥 Подтвердили: {count} человек\n\n"
        f"⚡ Crimea Light Monitor"
    )


    if message_id:

        await application.bot.edit_message_text(
            chat_id=CHANNEL_ID,
            message_id=message_id,
            text=text,
            parse_mode="HTML"
        )


    else:

        message = await application.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
            parse_mode="HTML"
        )


        save_alert(
            city,
            message.message_id
        )
