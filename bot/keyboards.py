from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def power_keyboard():

    keyboard = [
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

    return InlineKeyboardMarkup(keyboard)



def cities_keyboard():

    cities = [
        "Симферополь",
        "Ялта",
        "Керчь",
        "Севастополь",
        "Евпатория"
    ]

    keyboard = []

    for city in cities:
        keyboard.append(
            [
                InlineKeyboardButton(
                    city,
                    callback_data=f"city_{city}"
                )
            ]
        )

    return InlineKeyboardMarkup(keyboard)
