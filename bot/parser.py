import requests
from bs4 import BeautifulSoup


NEWS_PAGE = "https://crimea-energy.ru/about/news/"


KEYWORDS = [
    "электроснабж",
    "отключ",
    "обесточ",
    "огранич",
    "восстанов"
]


def get_latest_news():

    r = requests.get(
        NEWS_PAGE,
        timeout=10
    )

    r.encoding = "utf-8"


    soup = BeautifulSoup(
        r.text,
        "html.parser"
    )


    links = soup.find_all("a")


    for link in links:

        title = link.text.strip()


        if not title:
            continue


        text = title.lower()


        if any(
            word in text
            for word in KEYWORDS
        ):

            url = link.get("href")


            if url.startswith("/"):

                url = (
                    "https://crimea-energy.ru"
                    + url
                )


            return {
                "title": title,
                "url": url
            }


    return None


def parse_news(url):

    r = requests.get(
        url,
        timeout=10
    )

    r.encoding = "utf-8"

    soup = BeautifulSoup(
        r.text,
        "html.parser"
    )


    # весь текст страницы
    text = soup.get_text(
        "\n",
        strip=True
    )


    # ищем начало новости
    start_words = [
        "Из-за внешнего воздействия",
        "В связи с",
        "В результате"
    ]

    start = None

    for word in start_words:
        pos = text.find(word)

        if pos != -1:
            start = pos
            break


    if start is None:
        return "Не удалось найти текст новости"


    text = text[start:]


    # обрезаем конец мусора
    stop_words = [
        "Благодарим",
        "Телефон",
        "Адрес",
        "Пресс-служба",
        "Поделиться"
    ]


    for word in stop_words:

        pos = text.find(word)

        if pos != -1:
            text = text[:pos]


    # чистим строки

    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if (
            line
            and len(line) > 10
        ):
            lines.append(line)


    result = "\n\n".join(lines)


    return result[:1800]
