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

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_records = 0

    os.makedirs(DATA_DIR, exist_ok=True)

    # Основной способ — ищем все строки таблицы
    rows = soup.find_all('tr')

    with open(RAW_TXT, "a", encoding="utf-8") as f:
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 4:
                continue

            full_text = row.get_text(separator=" ", strip=True)

            if "1 BTC" not in full_text:
                continue

            try:
                # Название обменника — обычно первый td с текстом
                name_cell = cells[0].get_text(strip=True)
                name = re.sub(r'Данный обменный пункт.*$', '', name_cell, flags=re.IGNORECASE | re.DOTALL).strip()
                name = re.sub(r'\s+', ' ', name).strip()
                if len(name) < 3 or name in ["Обменник", ""]:
                    continue

                # Курс (RUB за 1 BTC)
                rate_match = re.search(r'(\d[\d\s,]*\.\d+|\d[\d\s,]*)', full_text)
                rate = rate_match.group(1).replace(' ', '').replace(',', '.') if rate_match else '0'

                # Резерв
                reserve_match = re.search(r'(\d[\d\s,]+)\s*RUB', full_text)
                reserve = reserve_match.group(1).replace(' ', '').replace(',', '') if reserve_match else '0'

                # Отзывы
                reviews_match = re.search(r'\[(\d+)\]', full_text)
                reviews = reviews_match.group(1) if reviews_match else '0'

                # Лимиты BTC
                btc_match = re.search(r'от\s*([\d\.]+)\s*до\s*([\d\.]+)', full_text)
                min_btc = btc_match.group(1) if btc_match else ''
                max_btc = btc_match.group(2) if btc_match else ''

                line = f"{now}|{name}|{rate}|{reserve}|{reviews}|{min_btc}|{max_btc}\n"
                f.write(line)
                new_records += 1

            except Exception:
                continue

    print(f"Найдено и добавлено обменников: {new_records}")
    return new_records


if __name__ == "__main__":
    scrape_bestchange()