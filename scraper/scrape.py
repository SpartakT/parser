import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

RAW_TXT = os.path.join(DATA_DIR, "raw_data.txt")


def scrape_bestchange():
    url = "https://www.bestchange.net/bitcoin-to-visa-mastercard-rub.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator="\n", strip=True)

    import re
    pattern = re.compile(
        r'([A-Za-zА-Яа-я0-9\s\-]+?)\s*1 BTC.*?от ([\d.]+) до ([\d.]+).*?([\d\s,]+) RUB Карта.*?([\d\s,]+)\s*\[(\d+)\]',
        re.DOTALL
    )

    matches = pattern.findall(text)
    print(f"Найдено {len(matches)} обменников")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_records = 0

    with open(RAW_TXT, "a", encoding="utf-8") as f:
        for m in matches:
            try:
                name = m[0].strip()
                min_btc = m[1]
                max_btc = m[2]
                rate = m[3].replace(" ", "").replace(",", ".")
                reserve = m[4].replace(" ", "").replace(",", "")
                reviews = m[5]

                line = f"{now}|{name}|{rate}|{reserve}|{reviews}|{min_btc}|{max_btc}\n"
                f.write(line)
                new_records += 1
            except:
                continue

    print(f"Добавлено {new_records} новых записей в raw_data.txt")
    return new_records