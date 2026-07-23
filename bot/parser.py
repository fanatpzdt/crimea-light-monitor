import re


CITIES = [
    "Симферополь",
    "Ялта",
    "Керчь",
    "Севастополь",
    "Евпатория",
    "Феодосия",
    "Бахчисарай",
    "Джанкой"
]


PROBLEMS = {
    "свет": "отключение света",
    "электр": "отключение света",
    "вод": "отключение воды",
    "газ": "проблемы с газом",
    "тепл": "нет отопления"
}


def parse_message(text):

    result = {
        "city": None,
        "district": None,
        "problem": None,
        "duration": None
    }


    text_lower = text.lower()


    # город
    for city in CITIES:
        if city.lower() in text_lower:
            result["city"] = city
            break


    # проблема
    for word, problem in PROBLEMS.items():
        if word in text_lower:
            result["problem"] = problem
            break


    # длительность
    duration = re.search(
        r"(\d+\s*(час|часа|часов|минут|минуты))",
        text_lower
    )

    if duration:
        result["duration"] = duration.group(1)


    # район
    districts = [
        "центр",
        "автовокзал",
        "старый город",
        "новый город"
    ]

    for district in districts:
        if district in text_lower:
            result["district"] = district.title()
            break


    return result
