from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def cities_keyboard():

    cities = [
        "Симферополь",
        "Севастополь",
        "Ялта",
        "Керчь",
        "Евпатория",
        "Феодосия",
        "Джанкой",
        "Красноперекопск",
        "Армянск",
        "Бахчисарай",
        "Алушта",
        "Белогорск",
        "Саки",
        "Судак",
        "Щёлкино"
    ]

    keyboard = []

    for city in cities:
        keyboard.append([
            InlineKeyboardButton(
                city,
                callback_data=f"city_{city}"
            )
        ])

    return InlineKeyboardMarkup(keyboard)


def power_keyboard():

    return InlineKeyboardMarkup([
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
    ])


def main_menu():

    return ReplyKeyboardMarkup(
        [
            ["⚡ Сообщить"],
            ["🏙 Выбрать другой город"],
            ["👤 Профиль"]
        ],
        resize_keyboard=True
    )


def profile_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🏙 Сменить город",
                callback_data="change_city"
            )
        ]
    ])
