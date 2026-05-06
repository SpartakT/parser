import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os

RAW_TXT = 'data/raw_data.txt'

def ensure_dir():
    os.makedirs('data', exist_ok=True)

def scrape_bestchange():
    url = "https://www.bestchange.com/bitcoin-to-visa-mastercard-rub.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
    }

    print("🔄 Запрашиваем данные с BestChange...")
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator="\n")

    pattern = re.compile(
        r'([A-Za-zА-Яа-я0-9\s\-]+?)\s+'
        r'This exchanger|This exchanger runs|This exchanger states|This exchanger does not fix|'
        r'(?:via third-party payment systems\.)?\s*'
        r'1 BTC\s*'
        r'min ([\d.]+)\s*'
        r'max ([\d.]+)\s*'
        r'([\d\s,]+) RUB Card\s*'
        r'([\d\s,]+?)\s*'
        r'\[(\d+)\]',
        re.IGNORECASE | re.DOTALL
    )

    exchangers = []
    matches = pattern.findall(text)

    print(f"Найдено потенциальных обменников: {len(matches)}")

    for match in matches:
        try:
            name = match[0].strip()
            min_btc = float(match[1])
            max_btc = float(match[2])
            rate_str = match[3].replace(' ', '').replace(',', '.')
            reserve_str = match[4].replace(' ', '').replace(',', '')
            reviews = int(match[5])

            rate = float(rate_str)

            exchangers.append({
                'timestamp': datetime.now().isoformat(),
                'exchanger': name,
                'rate': rate,
                'min_btc': min_btc,
                'max_btc': max_btc,
                'reserve': int(reserve_str),
                'reviews': reviews,
            })
        except:
            continue

    filtered = [ex for ex in exchangers if ex['reserve'] > 10_000_000 and ex['reviews'] > 100]

    print(f"Успешно спарсено: {len(exchangers)} | После фильтра: {len(filtered)}")
    return filtered


def save_raw_data(exchangers):
    if not exchangers:
        print("Нет данных для сохранения")
        return

    ensure_dir()
    with open(RAW_TXT, 'a', encoding='utf-8') as f:
        for ex in exchangers:
            line = (f"{ex['timestamp']}|{ex['exchanger']}|{ex['rate']}|"
                    f"{ex['min_btc']}|{ex['max_btc']}|{ex['reserve']}|{ex['reviews']}\n")
            f.write(line)

    print(f"Добавлено {len(exchangers)} новых записей в {RAW_TXT}")


if __name__ == "__main__":
    data = scrape_bestchange()
    save_raw_data(data)