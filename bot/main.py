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
    create_table,
    create_reports_table,
    create_alerts_table,
    create_users_table,
    save_user_city,
    get_user_city,
    save_report,
    get_city_stats,
    get_notifications,
    set_notifications
)

from channel import send_alert, restore_alert


# ---------------- START ----------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    city = get_user_city(user_id)

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

if data == "search_city":

    context.user_data["search_city"] = True

    await query.edit_message_text(
        "🔎 Введите первые буквы города:"
    )

    return
    
    print("КНОПКА:", data)

if data.startswith("found_"):

    city = data.replace(
        "found_",
        ""
    )


    save_user_city(
        query.from_user.id,
        city
    )


    await query.edit_message_text(
        f"✅ Город сохранён\n\n"
        f"📍 {city}",
        reply_markup=None
    )

    await query.message.reply_text(
        "Главное меню:",
        reply_markup=main_menu()
    )

    return
    
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

        city = get_user_city(
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

        city = get_user_city(
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


        count = get_city_stats(city)


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

        city = get_user_city(
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

if context.user_data.get("search_city"):

    results = search_city(text)

    context.user_data["search_city"] = False


    if not results:

        await update.message.reply_text(
            "Не нашёл город. Попробуйте ещё раз."
        )

        return


    from keyboards import search_result_keyboard


    await update.message.reply_text(
        "Выберите город:",
        reply_markup=search_result_keyboard(results)
    )

    return
    
    if text == "⚡ Сообщить":

        await update.message.reply_text(
            "Что произошло?",
            reply_markup=power_keyboard()
        )

        return



    if text == "👤 Профиль":

        city = get_user_city(
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

    create_table()
    create_reports_table()
    create_alerts_table()
    create_users_table()


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
