import os
from channel import publish, publish_restore
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from database import (
    create_table,
    create_reports_table,
    create_alerts_table,
create_city_status_table,
    save_report,
    get_city_stats,
    get_power_ok_count,
    set_city_status,
    get_city_status,
    set_power_start,
    get_power_start
)

from database import connect
from parser import parse_message
from keyboards import power_keyboard, cities_keyboard
from channel import publish
from config import ALERT_THRESHOLD

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "⚡ Crimea Light Monitor\n\n"
        "Что сейчас происходит?",
        reply_markup=power_keyboard()
    )
    
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    print("НАЖАТА КНОПКА:", query.data)

    await query.answer()

    print("ВСЕ ДАННЫЕ КНОПКИ:", query.data)
    
    if query.data.startswith("city_"):

        city = query.data.replace(
            "city_",
            ""
        )

        status = context.user_data.get("status")

        if not status:
            await query.edit_message_text(
                "Ошибка: сначала выберите состояние света"
            )
            return

        user_id = query.from_user.id

        save_report(
            user_id,
            city,
            status
        )

        set_city_status(
            city,
            status
        )

        if status == "no_power":
            set_power_start(city)

        count = get_city_stats(city)


        if status == "no_power":

            if count >= ALERT_THRESHOLD:

                await publish(
                    context.application,
                    city,
                    count
                )

            answer = (
                f"🔴 Записал\n\n"
                f"📍 {city}\n"
                f"Нет света\n\n"
                f"Подтвердили: {count} человек"
            )


        elif status == "power_ok":

            ok_count = get_power_ok_count(city)

            await publish_restore(
                context.application,
                city,
                ok_count
            )

            answer = (
                f"🟢 Записал\n\n"
                f"📍 {city}\n"
                f"Свет есть"
            )


        await query.edit_message_text(
            answer
        )
        
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.message.from_user.id


    data = parse_message(text)


    print("Распознано:")
    print(data)


    save_message(
        user_id=user_id,
        text=text,
        city=data["city"],
        district=data["district"],
        problem=data["problem"],
        duration=data["duration"]
    )
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT city, COUNT(*)
    FROM messages
    WHERE created_at >= datetime('now', '-24 hours')
    AND city IS NOT NULL
    GROUP BY city
    ORDER BY COUNT(*) DESC
    """)


    rows = cursor.fetchall()

    conn.close()


    if not rows:
        await update.message.reply_text(
            "За последние 24 часа сообщений нет"
        )
        return


    text = "⚡ Crimea Light Monitor\n\n"
    text += "За последние 24 часа:\n\n"


    for city, count in rows:
        text += f"🏙 {city}: {count} сообщений\n"


    await update.message.reply_text(text)

def main():
    create_table()
    create_reports_table()
    create_alerts_table()
    create_city_status_table()
    token = os.getenv("BOT_TOKEN")

    app = Application.builder().token(token).build()
    app.add_handler(
    CallbackQueryHandler(button)
    )
    app.add_handler(CommandHandler("start", start))

    app.add_handler(CommandHandler("stats", stats))

    app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        message
    )
    )

    print("Бот запущен")

    app.run_polling()


if __name__ == "__main__":
    main()
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    if query.data == "no_power":

        context.user_data["status"] = "no_power"

        await query.edit_message_text(
            "Выберите город:",
            reply_markup=cities_keyboard()
        )


    elif query.data == "power_ok":

        context.user_data["status"] = "power_ok"

        await query.edit_message_text(
            "Выберите город:",
            reply_markup=cities_keyboard()
        )
