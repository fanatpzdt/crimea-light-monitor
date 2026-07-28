import requests

url = "https://crimea-energy.ru/about/news/13406-o-vremennykh-ogranicheniyakh-elektrosnabzheniya"

r = requests.get(url)

with open("page.html", "w", encoding="utf-8") as f:
    f.write(r.text)

print("Страница сохранена")
