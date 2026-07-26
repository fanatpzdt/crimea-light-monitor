import os

from cities import search_city
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import ALERT_THRESHOLD

from keyboards import (
    cities_keyboard,
    power_keyboard,
    main_menu,
    profile_keyboard
)

from database import (
    init_db,
    save_city,
    get_city,
    save_report,
    count_no_power
)

from channel import send_alert, restore_alert


# ---------------- START ----------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    city = get_city(user_id)

    if city is None:

        await update.message.reply_text(
            "⚡ Crimea Light Monitor\n\n"
            "Выберите ваш город:",
            reply_markup=cities_keyboard()
        )

        return


    await update.message.reply_text(
        f"⚡ Crimea Light Monitor\n\n"
        f"📍 Ваш город: {city}",
        reply_markup=main_menu()
    )



# ---------------- BUTTONS ----------------


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

        await query.edit_message_text(
            f"✅ Город сохранён\n\n"
            f"📍 {city}\n\n"
            "Теперь можно сообщать о состоянии света."
        )

        return



    # смена города

    if data == "change_city":

        await query.edit_message_text(
            "Выберите новый город:",
            reply_markup=cities_keyboard()
        )

        return



    # профиль

    if data == "profile":

        city = get_city(
            query.from_user.id
        )

        await query.edit_message_text(
            f"👤 Профиль\n\n"
            f"📍 Город: {city or 'не выбран'}",
            reply_markup=profile_keyboard()
        )

        return



    # нет света

    if data == "no_power":

        city = get_city(
            query.from_user.id
        )

        if city is None:

            await query.edit_message_text(
                "Сначала выберите город."
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

            await send_alert(
                context.bot,
                city,
                count
            )


        await query.edit_message_text(
            f"🔴 Нет света\n\n"
            f"📍 {city}\n"
            f"👥 Подтвердили: {count}"
        )

        return



    # свет появился

    if data == "power_ok":

        city = get_city(
            query.from_user.id
        )

        if city:

            await restore_alert(
                context.bot,
                city
            )


        await query.edit_message_text(
            f"🟢 Свет есть\n\n"
            f"📍 {city}"
        )

        return



# ---------------- TEXT MENU ----------------


async def text_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    if text == "⚡ Сообщить":

        await update.message.reply_text(
            "Что произошло?",
            reply_markup=power_keyboard()
        )

        return



    if text == "👤 Профиль":

        city = get_city(
            update.message.from_user.id
        )

        await update.message.reply_text(
            f"👤 Профиль\n\n"
            f"📍 Город: {city or 'не выбран'}",
            reply_markup=profile_keyboard()
        )

        return



    if text == "🏙 Выбрать другой город":

        await update.message.reply_text(
            "Выберите город:",
            reply_markup=cities_keyboard()
        )

        return



# ---------------- RUN ----------------


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
        CallbackQueryHandler(
            button
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_menu
        )
    )


    print("Бот запущен")


    app.run_polling()



if __name__ == "__main__":
    main()
