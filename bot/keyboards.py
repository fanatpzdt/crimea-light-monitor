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
    "Севастополь",
    "Ялта",
    "Алушта",
    "Керчь",
    "Феодосия",
    "Евпатория",
    "Джанкой",
    "Армянск",
    "Красноперекопск",
    "Бахчисарай",
    "Белогорск",
    "Саки",
    "Судак",
    "Старый Крым",
    "Щёлкино",
    "Инкерман",
    "Гурзуф",
    "Массандра",
    "Ливадия",
    "Гаспра",
    "Кореиз",
    "Форос",
    "Коктебель",
    "Орджоникидзе",
    "Черноморское",
    "Раздольное",
    "Первомайское",
    "Красногвардейское",
    "Нижнегорский",
    "Советский",
    "Кировское",
    "Ленино",
    "Приморский",
    "Мирный",
    "Николаевка",
    "Новофёдоровка"
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
