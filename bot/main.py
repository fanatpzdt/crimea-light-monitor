import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from database import create_table, save_message
from parser import parse_message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚡ CrimeaLightBot запущен.\n"
        "Отправь сообщение об отключении света."
    )

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    save_message(
        user_id,
        text
    )
    print(f"Сохранено: {text}")

    await update.message.reply_text(
        f"Получено сообщение:\n{text}"
    )

def main():
    create_table()
    token = os.getenv("BOT_TOKEN")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message)
    )

    print("Бот запущен")

    app.run_polling()


if __name__ == "__main__":
    main()
