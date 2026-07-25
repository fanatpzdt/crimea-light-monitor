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
        ],
        [
            InlineKeyboardButton(
                "👤 Профиль",
                callback_data="profile"
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


def search_result_keyboard(results):

    keyboard = []

    for city in results:

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📍 {city}",
                    callback_data=f"found_{city}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "⬅️ Назад",
                callback_data="back_city"
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def profile_keyboard(notifications=True):

    keyboard = [
        [
            InlineKeyboardButton(
                "🏙 Сменить город",
                callback_data="change_city"
            )
        ]
    ]


    if notifications:

        keyboard.append(
            [
                InlineKeyboardButton(
                    "🔕 Отключить уведомления",
                    callback_data="notifications_off"
                )
            ]
        )

    else:

        keyboard.append(
            [
                InlineKeyboardButton(
                    "🔔 Включить уведомления",
                    callback_data="notifications_on"
                )
            ]
        )


    keyboard.append(
        [
            InlineKeyboardButton(
                "⬅️ Назад",
                callback_data="home"
            )
        ]
    )


    return InlineKeyboardMarkup(keyboard)
