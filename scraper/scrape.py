import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os
import ssl
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DATA_DIR = "data"
RAW_TXT = os.path.join(DATA_DIR, "raw_data.txt")


def scrape_bestchange():
    url = "https://www.bestchange.net/bitcoin-to-visa-mastercard-rub.html"

    session = requests.Session()

    class TLSAdapter(HTTPAdapter):
        def init_poolmanager(self, *args, **kwargs):
            ctx = ssl.create_default_context()
            ctx.minimum_version = ssl.TLSVersion.TLSv1_2
            ctx.set_ciphers('DEFAULT@SECLEVEL=1')
            kwargs['ssl_context'] = ctx
            return super().init_poolmanager(*args, **kwargs)

    session.mount('https://', TLSAdapter())

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    try:
        response = session.get(url, headers=headers, timeout=30, verify=False)  # verify=False — временно
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return 0

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator=" ", strip=True)

    pattern = r'([A-Za-zА-Яа-я0-9\s\.\-]+?)\s+1 BTC\s+от\s+([\d\.]+)\s+до\s+([\d\.]+)\s+([\d\s,]+)\s*RUB Карта\s+([\d\s,]+?)(?:\s*\[(\d+)\])?'

    matches = re.findall(pattern, text)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_records = 0

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(RAW_TXT, "a", encoding="utf-8") as f:
        for m in matches:
            try:
                name = re.sub(r'\s+Данный обменный пункт.*$', '', m[0].strip())
                rate = m[3].replace(" ", "").replace(",", ".")
                reserve = m[4].replace(" ", "").replace(",", "")
                reviews = m[5] if len(m) > 5 and m[5] else "0"
                min_btc = m[1]
                max_btc = m[2]

                line = f"{now}|{name}|{rate}|{reserve}|{reviews}|{min_btc}|{max_btc}\n"
                f.write(line)
                new_records += 1
            except:
                continue

    print(f"Найдено потенциальных обменников: {len(matches)}")
    print(f"Добавлено новых записей: {new_records}")
    return new_records