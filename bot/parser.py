import re


CITIES = [
    "Симферополь",
    "Севастополь",
    "Ялта",
    "Керчь",
    "Евпатория",
    "Феодосия",
    "Джанкой"
]


PROBLEMS = {
    "нет света": "Нет света",
    "отключили": "Нет света",
    "вырубили": "Нет света",
    "электричества нет": "Нет света",
    "свет моргает": "Мигает свет",
    "скачет напряжение": "Напряжение",
    "низкое напряжение": "Напряжение"
}


def parse_message(text):

    text_lower = text.lower()

    city = None

    for c in CITIES:
        if c.lower() in text_lower:
            city = c
            break

    problem = None

    for key, value in PROBLEMS.items():
        if key in text_lower:
            problem = value
            break

    duration = None

    m = re.search(r"(\d+)\s*(мин|час)", text_lower)

    if m:
        duration = m.group(0)

    return {
        "city": city,
        "district": None,
        "problem": problem,
        "duration": duration
    }
