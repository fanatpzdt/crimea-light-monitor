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


def parse_message(text):

    result = {
        "city": None,
        "district": None,
        "problem": None,
        "duration": None
    }


    text_lower = text.lower()


    # определяем город
    for city in CITIES:
        if city.lower() in text_lower:
            result["city"] = city
            break


    # определяем проблему
    if "свет" in text_lower or "электр" in text_lower:
        result["problem"] = "отключение света"


    # ищем время
    duration = re.search(
        r"(\d+\s*(час|часа|часов|минут|минуты))",
        text_lower
    )

    if duration:
        result["duration"] = duration.group(1)


    return result
