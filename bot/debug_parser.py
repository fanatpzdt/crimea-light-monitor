import requests
from bs4 import BeautifulSoup


url = "https://crimea-energy.ru/about/news/13406-0-vremennykh-ogranicheniy-elektrosnabzheniya"


r = requests.get(url)
r.encoding = "utf-8"

soup = BeautifulSoup(r.text, "html.parser")


for tag in soup.find_all(["article", "main", "div"]):
    text = tag.get_text(" ", strip=True)

    if "Действуют ограничения" in text:
        print("НАШЁЛ БЛОК:")
        print(text[:2000])
        break
