from cities import ALL_CITIES


def search_city(text):

    text = text.lower().strip()

    results = []

    for city in ALL_CITIES:

        if text in city.lower():

            results.append(city)

    return results[:5]
