import os

from parser import get_latest_news, parse_news


BASE_DIR = os.path.dirname(__file__)

LAST_FILE = os.path.join(
    BASE_DIR,
    "last_news.txt"
)


def get_last_url():

    if not os.path.exists(LAST_FILE):
        return ""

    with open(
        LAST_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return f.read().strip()



def save_last_url(url):

    with open(
        LAST_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(url)



def check_news():

    news = get_latest_news()

    if not news:
        return None


    last = get_last_url()


    if news["url"] == last:
        return None


    text = parse_news(
        news["url"]
    )


    save_last_url(
        news["url"]
    )


    return {
        "title": news["title"],
        "text": text,
        "url": news["url"]
    }
