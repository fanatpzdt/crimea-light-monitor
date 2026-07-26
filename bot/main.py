import os
import asyncio

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
from keyboards import (
    power_keyboard,
    cities_keyboard,
    search_result_keyboard,
    profile_keyboard,
    main_menu
)
from parser import parse_message

from channel import publish, publish_restore

from database import (
    connect,
    create_table,
    create_reports_table,
    create_alerts_table,
    create_users_table,
    save_user_city,
    get_user_city,
    create_city_status_table,
    create_power_events_table,
    save_report,
    save_message,
    get_city_stats,
    get_power_ok_count,
    set_city_status,
    set_power_start,
    get_notifications,
    set_notifications

)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    city = get_user_city(user_id)


    if city is None:

        context.user_data["profile_city"] = True

        await update.message.reply_text(
            "⚡ Crimea Light Monitor\n\n"
            "Выберите ваш населённый пункт:",
            reply_markup=cities_keyboard()
        )

        return


    await update.message.reply_text(
        f"⚡Crimea Light Monitor\n\n"
        f"📍 Ваш город: {city}\n\n"
        "Что сейчас происходит?",
        reply_markup=main_menu()
        )
    return

async def save_power_report(query, context, city):

    status = context.user_data.get("status")

    if status is None:
        await query.edit_message_text(
            "Сначала выберите действие"
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


    print("ГОРОД:", city)
    print("СТАТУС:", status)
    print("СЧЁТЧИК:", count)


    if status == "no_power":

        text = (
            f"🔴 Записано\n\n"
            f"📍 {city}\n"
            f"Нет света\n\n"
            f"👥 Подтвердили: {count}"
        )


    else:

        text = (
            f"🟢 Записано\n\n"
            f"📍 {city}\n"
            f"Свет есть"
        )


    await query.edit_message_text(
        text
    )
    
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    print("НАЖАТА КНОПКА:", query.data)


    # Поиск другого города

    if query.data == "search_city":

        context.user_data["search_mode"] = True

        await query.edit_message_text(
            "Введите первые буквы города:"
        )

        return


    # Нет света

    if query.data == "no_power":

        context.user_data["status"] = "no_power"

        city = get_user_city(
            query.from_user.id
        )

        if city:

            await save_power_report(
                query,
                context,
                city
            )

        else:

            await query.edit_message_text(
                "Выберите ваш город:",
                reply_markup=cities_keyboard()
            )

        return


    # Свет есть

    if query.data == "power_ok":

        context.user_data["status"] = "power_ok"

        city = get_user_city(
            query.from_user.id
        )

        if city:

            await save_power_report(
                query,
                context,
                city
            )

        else:

            await query.edit_message_text(
                "Выберите ваш город:",
                reply_markup=cities_keyboard()
            )

        return


    # Профиль

    if query.data == "profile":

        city = get_user_city(
            query.from_user.id
        )

        if city is None:
            city = "не выбран"

        await query.edit_message_text(
            f"👤 Ваш профиль\n\n"
            f"📍 Город: {city}\n\n"
            "Что хотите изменить?",
            reply_markup=profile_keyboard()
        )

        return
        
    if query.data == "notifications_off":

        set_notifications(
            query.from_user.id,
            0
        )


        await query.edit_message_text(
            "👤 Ваш профиль\n\n"
            f"📍 Город: {get_user_city(query.from_user.id)}\n"
            "🔕 Уведомления: выключены",
            reply_markup=profile_keyboard(False)
        )

        return



    if query.data == "notifications_on":

        set_notifications(
            query.from_user.id,
            1
        )


        await query.edit_message_text(
            "👤 Ваш профиль\n\n"
            f"📍 Город: {get_user_city(query.from_user.id)}\n"
            "🔔 Уведомления: включены",
            reply_markup=profile_keyboard(True)
        )

        return
        
    # Смена города

    if query.data == "change_city":

        context.user_data["profile_city"] = True

        await query.edit_message_text(
            "🏙 Выберите новый населённый пункт:",
            reply_markup=cities_keyboard()
        )

        return


    # Назад в главное меню

    if query.data == "home":

        city = get_user_city(
            query.from_user.id
        )

        if city is None:
            city = "не выбран"

        await query.edit_message_text(
            f"⚡ Crimea Light Monitor\n\n"
            f"📍 Ваш город: {city}\n\n"
            "Что сейчас происходит?",
            reply_markup=power_keyboard()
        )

        return


    city = None


    # Город из поиска

    if query.data.startswith("found_"):

        city = query.data.replace(
            "found_",
            ""
        )

        print("ПОИСК ВЫБРАЛ ГОРОД:", city)


    # Город из списка

    elif query.data.startswith("city_"):

        city = query.data.replace(
            "city_",
            ""
        )

        print("ВЫБРАН ГОРОД:", city)


    else:

        return


    # Если пользователь меняет или создаёт профиль

    if context.user_data.get("profile_city"):

        print("СОХРАНЯЕМ ГОРОД В ПРОФИЛЬ:", city)


        save_user_city(
            query.from_user.id,
            city
        )


        context.user_data["profile_city"] = False


        await query.edit_message_text(
            f"✅ Профиль обновлён\n\n"
            f"📍 Ваш город: {city}\n\n"
            "Теперь выберите действие:",
            reply_markup=power_keyboard()
        )

        return

    # Если город выбран, но действие не выбрано

    status = context.user_data.get("status")

    print("СТАТУС:", status)


    if status is None:

        await query.edit_message_text(
            "Сначала выберите действие:\n\n"
            "🔴 Нет света\n"
            "🟢 Свет есть"
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


    print("ГОРОД:", city)
    print("СТАТУС:", status)
    print("СЧЁТЧИК:", count)
    print("ЛИМИТ:", ALERT_THRESHOLD)



    # Отправка поста в канал

    if status == "no_power" and count >= ALERT_THRESHOLD:

        await publish(
            context.application,
            city,
            count
        )



    # Ответ пользователю

    if status == "no_power":

        text = (
            f"🔴 Записано\n\n"
            f"📍 {city}\n"
            f"Нет света\n\n"
            f"👥 Подтвердили: {count}"
        )


    else:

        text = (
            f"🟢 Записано\n\n"
            f"📍 {city}\n"
            f"Свет есть"
        )


    await query.edit_message_text(
        text
    )

    return
    
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.message.from_user.id
    
    if text == "⚡ Сообщить":

        await update.message.reply_text(
            "Выберите действие:",
            reply_markup=power_keyboard()
        )

        return


    if text == "👤 Профиль":

        city = get_user_city(
            update.message.from_user.id
        )

        notifications = get_notifications(
            update.message.from_user.id
        )


        await update.message.reply_text(
            f"👤 Ваш профиль\n\n"
            f"📍 Город: {city}\n\n"
            f"🔔 Уведомления: "
            f"{'включены' if notifications else 'выключены'}",
            reply_markup=profile_keyboard(
                notifications == 1
            )
        )

        return


    if text == "🏙 Мой город":

        city = get_user_city(
            update.message.from_user.id
        )

        await update.message.reply_text(
            f"📍 Ваш город: {city}",
            reply_markup=main_menu()
        )

        return
        
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

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    if text == "👤 Профиль":

        city = get_user_city(
            update.message.from_user.id
        )

        notifications = get_notifications(
            update.message.from_user.id
        )

        status = (
            "🔔 включены"
            if notifications
            else
            "🔕 выключены"
        )

        await update.message.reply_text(
            f"👤 Ваш профиль\n\n"
            f"📍 Город: {city}\n"
            f"{status}",
            reply_markup=profile_keyboard(notifications == 1)
        )

        return


    if text == "🏙 Мой город":

        city = get_user_city(
            update.message.from_user.id
        )

        await update.message.reply_text(
            f"📍 Ваш город: {city}",
            reply_markup=main_menu()
        )

        return


    if text == "⚡ Сообщить":

        await update.message.reply_text(
            "Выберите действие:",
            reply_markup=power_keyboard()
        )

        return
        
async def test_channel(application):

    await application.bot.send_message(
        chat_id="@energy_crimea",
        text="⚡ Тест: бот подключён к каналу."
    )
    
def main():

    create_table()
    create_reports_table()
    create_alerts_table()
    create_users_table()
    create_city_status_table()
    create_power_events_table()

    token = os.getenv("BOT_TOKEN")

    app = (
        Application.builder()
        .token(token)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .pool_timeout(30)
        .build()
    )

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

    asyncio.run(
    test_channel(app)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
