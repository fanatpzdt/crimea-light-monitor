import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from config import ALERT_THRESHOLD
from keyboards import cities_keyboard, power_keyboard

from database import (
    init_db,
    save_city,
    get_city,
    save_report,
    count_no_power
)

from channel import publish


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "⚡ Crimea Light Monitor\n\nВыберите город:",
        reply_markup=cities_keyboard()
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    print("КНОПКА:", data)


    # выбор города

    if data.startswith("city_"):

        city = data.replace(
            "city_",
            ""
        )

        save_user_city(
            query.from_user.id,
            city
        )

        await query.edit_message_text(
            f"📍 Город выбран: {city}\n\n"
            "Что произошло?",
            reply_markup=power_keyboard()
        )

        return



    # нет света

    if data == "no_power":

        city = get_user_city(
            query.from_user.id
        )

        if not city:

            await query.edit_message_text(
                "Сначала выберите город"
            )

            return


        save_report(
            query.from_user.id,
            city,
            "no_power"
        )


        count = get_city_stats(
            city
        )


        print(
            "ГОРОД:",
            city,
            "СЧЁТ:",
            count
        )


        if count >= ALERT_THRESHOLD:

            print("ОТПРАВЛЯЮ ПОСТ")

            await publish(
                context.application,
                city,
                count
            )


        await query.edit_message_text(
            f"🔴 Нет света\n\n"
            f"📍 {city}\n"
            f"👥 Подтвердили: {count}"
        )


        return



    # свет есть

    if data == "power_ok":

        city = get_user_city(
            query.from_user.id
        )


        await query.edit_message_text(
            f"🟢 Свет есть\n\n"
            f"📍 {city}"
        )


def main():

    create_table()
    create_reports_table()
    create_users_table()


    token = os.getenv(
        "BOT_TOKEN"
    )


    app = (
        Application.builder()
        .token(token)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .pool_timeout(30)
        .build()
    )


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            button
        )
    )


    print(
        "Бот запущен"
    )


    app.run_polling()



if __name__ == "__main__":
    main()
