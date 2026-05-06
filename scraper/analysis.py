import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

DATA_DIR = "data"
ARTIFACTS_DIR = "artifacts"

if not os.path.exists(ARTIFACTS_DIR):
    os.makedirs(ARTIFACTS_DIR)

RAW_TXT = os.path.join(DATA_DIR, "raw_data.txt")


def run_analysis():
    if not os.path.exists(RAW_TXT):
        print("Нет файла raw_data.txt")
        return

    with open(RAW_TXT, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    print(f"Анализ данных на момент: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Всего строк в файле: {len(lines)}")

    filtered = []
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 6:
            continue

        try:
            name = parts[1].strip()
            rate = float(parts[2])
            reserve = int(parts[3])
            reviews = int(parts[4])

            if reserve > 500_000 and reviews >= 100:
                filtered.append({
                    "name": name,
                    "rate": rate,
                    "reserve": reserve,
                    "reviews": reviews,
                    "min_btc": parts[5] if len(parts) > 5 else "",
                    "max_btc": parts[6] if len(parts) > 6 else ""
                })
        except:
            continue

    print(f"Под фильтр подошло {len(filtered)} обменников")

    if not filtered:
        print("Нет данных для анализа.")
        return

    df = pd.DataFrame(filtered)

    csv_path = os.path.join(ARTIFACTS_DIR, "bestchange_top.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")

    # График
    plt.figure(figsize=(12, 6))
    top10 = df.nlargest(10, 'reserve')
    plt.barh(top10['name'].str[:25], top10['reserve'])
    plt.xlabel('Резерв (RUB)')
    plt.ylabel('Обменник')
    plt.title('Топ-10 обменников по резерву (BTC → RUB)')
    plt.tight_layout()
    plt.savefig(os.path.join(ARTIFACTS_DIR, "top_reserve.png"))
    plt.close()

    print("Артефакты успешно созданы в папке artifacts/")


if __name__ == "__main__":
    run_analysis()