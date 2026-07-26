import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from database import (
    init_db,
    save_city,
    get_city,
    save_report,
    count_no_power
)

from keyboards import (
    cities_keyboard,
    power_keyboard,
    main_menu
)

from channel import publish

from config import ALERT_THRESHOLD


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    city = get_city(user_id)

    if city is None:

        context.user_data["select_city"] = True

        await update.message.reply_text(
            "⚡ Crimea Light Monitor\n\n"
            "Выберите ваш город:",
            reply_markup=cities_keyboard()
        )

        return


    await update.message.reply_text(
        f"⚡ Crimea Light Monitor\n\n"
        f"📍 Ваш город: {city}\n\n"
        "Что происходит?",
        reply_markup=main_menu()
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

        save_city(
            query.from_user.id,
            city
        )


        context.user_data["city"] = city


        await query.edit_message_text(
            f"✅ Город сохранён\n\n"
            f"📍 {city}\n\n"
            "Выберите действие:",
            reply_markup=power_keyboard()
        )

        return



    # нет света

    if data == "no_power":

        city = get_city(
            query.from_user.id
        )


        if city is None:

            await query.edit_message_text(
                "Сначала выберите город",
                reply_markup=cities_keyboard()
            )

            return


        save_report(
            query.from_user.id,
            city,
            "no_power"
        )


        count = count_no_power(city)


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
            f"🔴 Записано\n\n"
            f"📍 {city}\n"
            f"Нет света\n\n"
            f"👥 Подтвердили: {count}"
        )

        return



    # свет есть

    if data == "power_ok":

        city = get_city(
            query.from_user.id
        )


        if city is None:

            await query.edit_message_text(
                "Сначала выберите город"
            )

            return


        save_report(
            query.from_user.id,
            city,
            "power_ok"
        )


        await query.edit_message_text(
            f"🟢 Записано\n\n"
            f"📍 {city}\n"
            "Свет есть"
        )

        return



async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    if text == "⚡ Сообщить":

        await update.message.reply_text(
            "Выберите:",
            reply_markup=power_keyboard()
        )

        return


    if text == "🏙 Мой город":

        city = get_city(
            update.message.from_user.id
        )


        await update.message.reply_text(
            f"📍 Ваш город: {city}",
            reply_markup=main_menu()
        )

        return



async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Статистика временно отключена"
    )



def main():

    init_db()


    token = os.getenv(
        "BOT_TOKEN"
    )


    app = (
        Application.builder()
        .token(token)
        .build()
    )


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CommandHandler(
            "stats",
            stats
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            button
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
