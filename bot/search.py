from cities.py import cities


def search_city(text):

    text = text.lower().strip()

    result = []

    for city in cities:

        if city.lower().startswith(text):
            result.append(city)

    return result[:10]
