from config import CHANNEL_ID
from database import connect


async def publish(application, city, count):

    text = (
        "⚡ <b>Отключение электроэнергии</b>\n\n"
        f"📍 <b>{city}</b>\n\n"
        "🔴 Свет отсутствует\n\n"
        f"👥 Подтвердили: {count}\n\n"
        "⚡ Crimea Light Monitor"
    )


    msg = await application.bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        parse_mode="HTML"
    )


    db = connect()
    cur = db.cursor()


    cur.execute(
        """
        INSERT OR REPLACE INTO alerts
        VALUES (?,?)
        """,
        (
            city,
            msg.message_id
        )
    )


    db.commit()
    db.close()
