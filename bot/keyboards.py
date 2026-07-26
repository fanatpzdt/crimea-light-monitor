from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from cities import popular_cities


# Популярные города при старте

def cities_keyboard():

    buttons = []

    for city in popular_cities():

        buttons.append(
            [
                InlineKeyboardButton(
                    city,
                    callback_data=f"city_{city}"
                )
            ]
        )


    buttons.append(
        [
            InlineKeyboardButton(
                "🔎 Выбрать другой город",
                callback_data="search_city"
            )
        ]
    )


    return InlineKeyboardMarkup(buttons)



# Результаты поиска города

def search_result_keyboard(cities):

    buttons = []


    for city in cities:

        buttons.append(
            [
                InlineKeyboardButton(
                    city,
                    callback_data=f"found_{city}"
                )
            ]
        )


    buttons.append(
        [
            InlineKeyboardButton(
                "⬅️ Назад",
                callback_data="back"
            )
        ]
    )


    return InlineKeyboardMarkup(buttons)



# Выбор света

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
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Назад",
                    callback_data="back"
                )
            ]
        ]
    )


# Профиль

def profile_keyboard(notifications=True):

    notify = (
        "🔕 Выключить уведомления"
        if notifications
        else
        "🔔 Включить уведомления"
    )


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
                    notify,
                    callback_data=(
                        "notifications_off"
                        if notifications
                        else
                        "notifications_on"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Назад",
                    callback_data="back"
                )
            ]
        ]
    )



# Нижняя постоянная клавиатура

def main_menu():

    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("⚡ Сообщить"),
                KeyboardButton("👤 Профиль")
            ]
        ],
        resize_keyboard=True
    )
