from keyboards import power_keyboard


async def start(update, context):

    await update.message.reply_text(
        "⚡ Crimea Light Monitor\n\n"
        "Сообщите о наличии электроэнергии",
        reply_markup=power_keyboard()
    )
