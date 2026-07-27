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


    # удаляем мусор
    for tag in soup.find_all(
        [
            "script",
            "style",
            "header",
            "footer",
            "nav"
        ]
    ):
        tag.decompose()


    paragraphs = []

    for p in soup.find_all("p"):

        text = p.get_text(
            " ",
            strip=True
        )

        if not text:
            continue


        # берём только полезные строки
        if len(text) > 20:

            paragraphs.append(text)


    result = "\n\n".join(paragraphs)


    # ограничение для Telegram
    return result[:2500]
