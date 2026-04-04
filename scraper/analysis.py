import os
from datetime import datetime

ARTIFACTS_DIR = "artifacts"
if not os.path.exists(ARTIFACTS_DIR):
    os.makedirs(ARTIFACTS_DIR)

RAW_TXT = "data/raw_data.txt"

def run_analysis():
    if not os.path.exists(RAW_TXT):
        print("Файл raw_data.txt ещё пустой.")
        return 0
    with open(RAW_TXT, "r", encoding="utf-8") as f:
        lines = f.readlines()
    filtered = []
    for line in lines:
        parts = line.strip().split("|")
        if len(parts) != 7:
            continue

        try:
            reserve = int(parts[3])
            reviews = int(parts[4])
            if reserve > 10_000_000 and reviews > 5000:
                filtered.append(parts)
        except:
            continue
    print(f"Под фильтр подошло {len(filtered)} обменников")

    now = datetime.now().strftime("%Y%m%d_%H%M")
    filtered_file = f"artifacts/filtered_{now}.txt"

    with open(filtered_file, "w", encoding="utf-8") as f:
        f.write("timestamp|name|rate|reserve|reviews|min_btc|max_btc\n")
        for item in filtered:
            f.write("|".join(item) + "\n")

    print(f"Отфильтрованный файл сохранён: {filtered_file}")

    print("\nТОП-5 лучших по курсу:")
    sorted_list = sorted(filtered, key=lambda x: float(x[2]), reverse=True)
    for i, item in enumerate(sorted_list[:5], 1):
        print(f"{i}. {item[1]} → курс {item[2]} RUB | резерв {item[3]} | отзывов {item[4]}")

    return len(filtered)