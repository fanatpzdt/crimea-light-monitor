with open("page.html", "r", encoding="utf-8") as f:
    html = f.read()

for word in [
    "Энергетики",
    "Благодарим",
    "Поделиться",
    "огранич",
]:
    print(word, html.find(word))
