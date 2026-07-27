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


    # убираем мусор
    for tag in soup(
        [
            "script",
            "style",
            "header",
            "footer",
            "nav"
        ]
    ):
        tag.decompose()


    # ищем основной текст новости
    article = soup.find(
        "article"
    )


    if article:

        text = article.get_text(
            "\n",
            strip=True
        )

    else:

        text = soup.get_text(
            "\n",
            strip=True
        )


    # убираем пустые строки
    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line:
            lines.append(line)


    return "\n\n".join(lines)
