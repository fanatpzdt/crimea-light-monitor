from config import CHANNEL_ID
from database import connect


async def send_alert(bot,city,count):


    text=f"""
⚡ <b>Отключение электроэнергии</b>

📍 <b>{city}</b>

🔴 Свет отсутствует

👥 Подтвердили: {count}

Crimea Light Monitor
"""


    msg=await bot.send_message(
        CHANNEL_ID,
        text,
        parse_mode="HTML"
    )


    db=connect()
    cur=db.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO alerts
        VALUES(?,?)
        """,
        (
            city,
            msg.message_id
        )
    )

    db.commit()
    db.close()
