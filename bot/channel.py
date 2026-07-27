import os

from telegram.constants import ParseMode
from config import CHANNEL_ID
from database import connect

async def send_alert(bot, city, count):
    text = (
        "⚡ <b>Отключение электроэнергии</b>\n\n"
        f"📍 <b>{city}</b>\n\n"
        "🔴 Свет отсутствует\n"
        f"👥 Подтвердили: {count}\n\n"
        "Crimea Light Monitor"
    )

    msg = await bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        parse_mode=ParseMode.HTML
    )

    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO alerts(city, message_id)
        VALUES(?,?)
        """,
        (city, msg.message_id)
    )

    db.commit()
    db.close()


async def restore_alert(bot, city):
    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT message_id FROM alerts WHERE city=?",
        (city,)
    )

    row = cur.fetchone()

    if row:
        await bot.edit_message_text(
            chat_id=CHANNEL_ID,
            message_id=row[0],
            text=(
                "🟢 <b>Электроснабжение восстановлено</b>\n\n"
                f"📍 <b>{city}</b>\n\n"
                "✅ Свет появился\n\n"
                "Crimea Light Monitor"
            ),
            parse_mode=ParseMode.HTML
        )

        cur.execute(
            "DELETE FROM alerts WHERE city=?",
            (city,)
        )

        db.commit()

    db.close()

NEWS_CHANNEL_ID = os.getenv("NEWS_CHANNEL_ID")


async def send_news(bot, news):

    message = (
        f"⚡ <b>{news['title']}</b>\n\n"
        f"{news['text'][:3500]}\n\n"
        f"🔗 Источник:\n{news['url']}"
    )

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=False
    )
