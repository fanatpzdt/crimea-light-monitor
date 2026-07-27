from parser import get_latest_news, parse_news


news = get_latest_news()

print(news)


if news:

    text = parse_news(
        news["url"]
    )

    print("\n---НОВОСТЬ---\n")

    print(
        text[:2000]
    )
