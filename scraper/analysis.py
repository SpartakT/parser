import pandas as pd
import matplotlib.pyplot as plt
import re
import os
from datetime import datetime

DATA_DIR = "data"
ARTIFACTS_DIR = "artifacts"

if not os.path.exists(ARTIFACTS_DIR):
    os.makedirs(ARTIFACTS_DIR)

RAW_TXT = os.path.join(DATA_DIR, "raw_data.txt")


def clean_name(name):
    name = re.sub(r'^\s*[\d\s]{6,}', '', name)
    name = re.sub(r'Резерв Отзывы ', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def run_analysis():
    with open(RAW_TXT, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    print(f"Анализ данных на момент: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Всего строк: {len(lines)}")

    data = []
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 7:
            continue
        try:
            name = clean_name(parts[1].strip())
            if len(name) < 3:
                continue

            rate = float(str(parts[2]).replace(" ", "").replace(",", "."))
            reserve = int(float(str(parts[3]).replace(" ", "").replace(",", "")))
            reviews = int(parts[4])

            if rate < 1000 or rate > 7000000 or reserve < 1:
                continue

            data.append({
                "name": name,
                "rate": rate,
                "reserve": reserve,
                "reviews": reviews,
                "min_btc": parts[5],
                "max_btc": parts[6]
            })
        except:
            continue

    print(f"Валидных обменников: {len(data)}")

    df = pd.DataFrame(data)
    df.to_csv(os.path.join(ARTIFACTS_DIR, "bestchange_top.csv"), index=False, encoding="utf-8")

    if len(df) == 0:
        print("Нет данных")
        return

    df_top_reserve = df.nlargest(10, 'reserve')
    df_top_rate = df.nlargest(10, 'rate')

    # Графики
    plt.figure(figsize=(14, 8))
    plt.barh(df_top_reserve['name'].str[:42], df_top_reserve['reserve'])
    plt.xlabel('Резерв (RUB)')
    plt.ylabel('Обменник')
    plt.title('Топ-10 обменников по резерву (BTC → RUB)')
    plt.tight_layout()
    plt.savefig(os.path.join(ARTIFACTS_DIR, "top_reserve.png"))
    plt.close()

    plt.figure(figsize=(14, 8))
    plt.barh(df_top_rate['name'].str[:42], df_top_rate['rate'])
    plt.xlabel('Курс (RUB за 1 BTC)')
    plt.ylabel('Обменник')
    plt.title('Топ-10 обменников по курсу')
    plt.tight_layout()
    plt.savefig(os.path.join(ARTIFACTS_DIR, "top_rate.png"))
    plt.close()

    print(f"Артефакты созданы в {ARTIFACTS_DIR}/")
    print("Рекомендуемые графики: top_reserve.png и top_rate.png")


if __name__ == "__main__":
    run_analysis()