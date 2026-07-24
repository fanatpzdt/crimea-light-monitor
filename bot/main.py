import os

from cities import search_city
from search import search_city
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import ALERT_THRESHOLD
from keyboards import power_keyboard, cities_keyboard
from parser import parse_message

from channel import publish, publish_restore

from database import (
    connect,
    create_table,
    create_reports_table,
    create_alerts_table,
    create_city_status_table,
    create_power_events_table,
    save_report,
    save_message,
    get_city_stats,
    get_power_ok_count,
    set_city_status,
    set_power_start,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚡ Crimea Light Monitor\n\n"
        "Что сейчас происходит?",
        reply_markup=power_keyboard()
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    print("НАЖАТА КНОПКА:", query.data)


    if query.data == "search_city":

        context.user_data["search_mode"] = True

        await query.edit_message_text(
            "Введите первые буквы города:"
        )

        return


    if query.data == "no_power":

        context.user_data["status"] = "no_power"

        await query.edit_message_text(
            "Выберите город:",
            reply_markup=cities_keyboard()
        )

        return


    if query.data == "power_ok":

        context.user_data["status"] = "power_ok"

        await query.edit_message_text(
            "Выберите город:",
            reply_markup=cities_keyboard()
        )

        return


    if query.data.startswith("city_"):

        city = query.data.replace(
            "city_",
            ""
        )

        print("ГОРОД:", city)

        status = context.user_data.get("status")

        print("СТАТУС:", status)

        if status is None:

            await query.edit_message_text(
                "Ошибка. Нажмите /start"
            )

            return

        await query.edit_message_text(
            f"Вы выбрали: {city}"
        )

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.message.from_user.id
    if context.user_data.get("search_mode"):

        results = search_city(text)

        if results:

            keyboard = []

            for city in results:
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            city,
                            callback_data=f"city_{city}"
                        )
                    ]
                )

            await update.message.reply_text(
                "Нашёл города:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        else:

            await update.message.reply_text(
                "Город не найден. Попробуйте ещё раз."
            )

        return
        
    if context.user_data.get("search_mode"):

        results = search_city(text)

        if results:

            await update.message.reply_text(
                "Нашёл города:\n\n" +
                "\n".join(
                    f"📍 {city}" for city in results
                )
            )

        else:

            await update.message.reply_text(
                "Город не найден"
            )

        context.user_data["search_mode"] = False

        return


    data = parse_message(text)

    save_message(
        user_id=user_id,
        text=text,
        city=data["city"],
        district=data["district"],
        problem=data["problem"],
        duration=data["duration"],
    )


    await update.message.reply_text(
        "Спасибо, сообщение сохранено."
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT city, COUNT(*)
        FROM reports
        GROUP BY city
        ORDER BY COUNT(*) DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:

        await update.message.reply_text(
            "Статистика пока пустая."
        )

        return

    text = "⚡ Статистика\n\n"

    for city, count in rows:
        text += f"{city}: {count}\n"

    await update.message.reply_text(text)


def main():

    create_table()
    create_reports_table()
    create_alerts_table()
    create_city_status_table()
    create_power_events_table()
    
    token = os.getenv("BOT_TOKEN")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button))
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
