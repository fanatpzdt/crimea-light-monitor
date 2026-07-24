import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from database import (
    create_table,
    create_reports_table,
    create_alerts_table,
    create_city_status_table,
    save_report,
    get_city_stats,
    get_power_ok_count,
    set_city_status,
    set_power_start,
    save_message,
    connect
)

from keyboards import power_keyboard, cities_keyboard
from channel import publish, publish_restore
from parser import parse_message
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


    # пользователь нажал "Нет света"
    if query.data == "no_power":

        context.user_data["status"] = "no_power"

        await query.edit_message_text(
            "Выберите город:",
            reply_markup=cities_keyboard()
        )

        return


    # пользователь нажал "Свет есть"
    if query.data == "power_ok":

        context.user_data["status"] = "power_ok"

        await query.edit_message_text(
            "Выберите город:",
            reply_markup=cities_keyboard()
        )

        return


    # пользователь выбрал город
    if query.data.startswith("city_"):

        print("ГОРОД НАЖАТ:", query.data)

        city = query.data.replace(
            "city_",
            ""
        )

        status = context.user_data.get("status")

        print("СТАТУС:", status)
        print("ГОРОД:", city)

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

        count = get_city_stats(city)

        answer = (
            f"Записал\n\n"
            f"Город: {city}\n"
            f"Статус: {status}\n"
            f"Подтвердили: {count}"
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
    WHERE created_at >= datetime('now','-24 hours')
    AND city IS NOT NULL
    GROUP BY city
    ORDER BY COUNT(*) DESC
    """)


    rows = cursor.fetchall()


    conn.close()


    if not rows:

        await update.message.reply_text(
            "Сообщений нет"
        )

        return


    text = "⚡ Статистика:\n\n"


    for city, count in rows:

        text += f"{city}: {count}\n"


    await update.message.reply_text(text)



def main():

    create_table()
    create_reports_table()
    create_alerts_table()
    create_city_status_table()


    token = os.getenv("BOT_TOKEN")


    app = Application.builder().token(token).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CallbackQueryHandler(button)
    )


    app.add_handler(
        CommandHandler(
            "stats",
            stats
        )
    )


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
