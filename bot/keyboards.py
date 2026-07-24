from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from cities import POPULAR_CITIES


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

    keyboard = []


    for city in POPULAR_CITIES:

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"🏙 {city}",
                    callback_data=f"city_{city}"
                )
            ]
        )


    keyboard.append(
        [
            InlineKeyboardButton(
                "🔍 Найти другой населённый пункт",
                callback_data="search_city"
            )
        ]
    )


    return InlineKeyboardMarkup(keyboard)
