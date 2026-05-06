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
    rows = soup.select('tr')

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_records = 0

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(RAW_TXT, "a", encoding="utf-8") as f:
        for row in rows:
            text = row.get_text(separator="|", strip=True)
            if "1 BTC" not in text or len(text) < 50:
                continue

            parts = [p.strip() for p in text.split('|') if p.strip()]

            try:
                name = parts[0]
                name = re.sub(r'Данный обменный пункт.*$', '', name, flags=re.IGNORECASE).strip()
                name = re.sub(r'\s+', ' ', name).strip()

                rate_match = re.search(r'(\d[\d\s,]*\.\d+|\d[\d\s,]*)', ' '.join(parts[1:]))
                rate = rate_match.group(1).replace(' ', '').replace(',', '.') if rate_match else '0'

                reserve_match = re.search(r'(\d[\d\s,]+)\s*RUB', ' '.join(parts))
                reserve = reserve_match.group(1).replace(' ', '').replace(',', '') if reserve_match else '0'

                reviews_match = re.search(r'\[(\d+)\]', ' '.join(parts))
                reviews = reviews_match.group(1) if reviews_match else '0'

                btc_limits = re.findall(r'от\s*([\d\.]+)\s*до\s*([\d\.]+)', ' '.join(parts))
                min_btc = btc_limits[0][0] if btc_limits else ''
                max_btc = btc_limits[0][1] if btc_limits else ''

                line = f"{now}|{name}|{rate}|{reserve}|{reviews}|{min_btc}|{max_btc}\n"
                f.write(line)
                new_records += 1

            except Exception:
                continue

    print(f"Найдено и добавлено обменников: {new_records}")
    return new_records


if __name__ == "__main__":
    scrape_bestchange()