import requests


url = "https://crimea-energy.ru/about/news/13406-o-vremennykh-ogranicheniyakh-elektrosnabzheniya"


r = requests.get(
    url,
    timeout=10
)

r.encoding = "utf-8"


html = r.text


for word in [
    "Действуют ограничения",
    "Энергетики",
    "обесточена"
]:

    pos = html.find(word)

    print(
        word,
        "позиция:",
        pos
    )

    if pos != -1:
        print(
            html[pos-500:pos+1000]
        )
