from config import CHANNEL_ID
from database import get_alert, save_alert


async def publish(application, city, count):

    message_id = get_alert(city)


    text = (
    "⚡ <b>Сообщение о перебое электроснабжения</b>\n\n"
    f"📍 Населённый пункт: <b>{city}</b>\n"
    "🔴 Статус: отсутствует электроснабжение\n\n"
    f"👥 Подтвердили пользователи: <b>{count}</b>\n\n"
    "ℹ️ Информация получена от жителей через Crimea Light Monitor.\n"
    "Следим за развитием ситуации."
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



async def publish_restore(application, city, count):


    message_id = get_alert(city)


    if not message_id:

        return



    text = (
        f"🟢 <b>{city}</b>\n\n"
        f"Электроснабжение восстановлено\n\n"
        f"👥 Подтвердили: {count} человек\n\n"
        f"⚡ Crimea Light Monitor"
    )


    await application.bot.edit_message_text(
        chat_id=CHANNEL_ID,
        message_id=message_id,
        text=text,
        parse_mode="HTML"
    )
