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


    text = soup.get_text(
        "\n"
    )


    return text

if __name__ == "__main__":
    news = get_latest_news()

    if not news:
        print("Новости не найдены")
    else:
        print("Заголовок:", news["title"])
        print("Ссылка:", news["url"])
        print()

        text = parse_news(news["url"])
        print(text[:2000])
