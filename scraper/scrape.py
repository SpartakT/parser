import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os

DATA_DIR = "data"
RAW_TXT = os.path.join(DATA_DIR, "raw_data.txt")


def scrape_bestchange():
    url = "https://www.bestchange.net/bitcoin-to-visa-mastercard-rub.html"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=40)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return 0

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator="\n", strip=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_records = 0

    os.makedirs(DATA_DIR, exist_ok=True)
    open(RAW_TXT, "w", encoding="utf-8").close()

    pattern = r'([^\n]+?)\s+1 BTC\s+от\s+([\d\.]+)\s+до\s+([\d\.]+).*?(\d[\d\s,]+)\s*RUB.*?Карта.*?(\d+)'

    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

    with open(RAW_TXT, "a", encoding="utf-8") as f:
        for m in matches:
            try:
                name = m[0].strip()
                name = re.sub(r'Данный обменный пункт.*$', '', name, flags=re.IGNORECASE).strip()
                name = re.sub(r'\s+', ' ', name).strip()

                if len(name) < 3:
                    continue

                rate = "0"
                reserve = m[3].replace(" ", "").replace(",", "")
                reviews = m[4] if len(m) > 4 else "0"
                min_btc = m[1]
                max_btc = m[2]

                line = f"{now}|{name}|{rate}|{reserve}|{reviews}|{min_btc}|{max_btc}\n"
                f.write(line)
                new_records += 1

            except Exception:
                continue

    print(f"Найдено и добавлено обменников: {new_records}")
    return new_records


if __name__ == "__main__":
    scrape_bestchange()