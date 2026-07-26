from telegram import InlineKeyboardButton,InlineKeyboardMarkup


def cities_keyboard():

    cities=[
        "Симферополь",
        "Севастополь",
        "Ялта",
        "Керчь"
    ]

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    c,
                    callback_data=f"city_{c}"
                )
            ]
            for c in cities
        ]
    )


def power_keyboard():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔴 Нет света",
                    callback_data="no_power"
                )
            ],
            [
                InlineKeyboardButton(
                    "🟢 Свет есть",
                    callback_data="power_ok"
                )
            ]
        ]
    )
