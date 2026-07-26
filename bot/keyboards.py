from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def cities_keyboard():
    cities = [
        "Симферополь",
        "Севастополь",
        "Ялта",
        "Керчь",
        "Евпатория",
        "Феодосия",
        "Алушта",
        "Бахчисарай",
        "Джанкой",
        "Красноперекопск",
        "Армянск",
        "Саки",
        "Белогорск",
        "Щёлкино",
        "Судак"
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

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔍 Найти город",
                callback_data="search_city"
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


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
                    "🟢 Свет появился",
                    callback_data="power_ok"
                )
            ]
        ]
    )


def main_menu():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⚡ Сообщить",
                    callback_data="report"
                )
            ],
            [
                InlineKeyboardButton(
                    "👤 Профиль",
                    callback_data="profile"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏙 Сменить город",
                    callback_data="change_city"
                )
            ]
        ]
    )


def profile_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🏙 Сменить город",
                    callback_data="change_city"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Назад",
                    callback_data="home"
                )
            ]
        ]
    )
