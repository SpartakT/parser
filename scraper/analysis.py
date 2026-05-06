import os
from datetime import datetime
from pathlib import Path

from prefect.artifacts import create_markdown_artifact, create_table_artifact
import matplotlib.pyplot as plt

ARTIFACTS_DIR = "artifacts"
Path(ARTIFACTS_DIR).mkdir(exist_ok=True)

RAW_TXT = "data/raw_data.txt"


def run_analysis():
    if not os.path.exists(RAW_TXT):
        create_markdown_artifact(
            markdown="## Ошибка\nФайл raw_data.txt ещё пустой.\nСначала запустите скрапер.",
            key="analysis-error",
            description="Ошибка анализа"
        )
        print("Файл raw_data.txt ещё пустой.")
        return 0

    with open(RAW_TXT, "r", encoding="utf-8") as f:
        lines = f.readlines()

    latest_timestamp = None
    latest_records = []

    for line in lines:
        if not line.strip():
            continue
        parts = line.strip().split("|")
        if len(parts) != 7:
            continue

        ts = parts[0]
        if latest_timestamp is None or ts > latest_timestamp:
            latest_timestamp = ts
            latest_records = [parts]
        elif ts == latest_timestamp:
            latest_records.append(parts)

    if not latest_records:
        print("Нет данных для анализа.")
        return 0

    print(f"Анализ данных на момент: {latest_timestamp}")

    filtered = []
    for parts in latest_records:
        try:
            reserve = int(parts[3])
            reviews = int(parts[4])
            rate = float(parts[2])

            if reserve > 1_000_000 and reviews > 100:
                filtered.append({
                    "name": parts[1],
                    "rate": rate,
                    "reserve": reserve,
                    "reviews": reviews,
                    "min_btc": parts[5],
                    "max_btc": parts[6]
                })
        except ValueError:
            continue

    count = len(filtered)
    print(f"Под фильтр подошло {count} обменников")

    now = datetime.now().strftime("%Y%m%d_%H%M")

    markdown = f"""
# BestChange Анализ

**Время анализа:** {latest_timestamp}  
**Отфильтровано:** {count} обменников

### ТОП-5 лучших по курсу:
"""

    if filtered:
        top5 = sorted(filtered, key=lambda x: x["rate"], reverse=True)[:5]
        for i, item in enumerate(top5, 1):
            markdown += f"{i}. {item['name']} → {item['rate']} RUB | резерв {item['reserve']} | отзывов {item['reviews']}\n"

    create_markdown_artifact(
        markdown=markdown.strip(),
        key="bestchange-summary",
        description=f"Анализ BestChange — {latest_timestamp}"
    )

    if filtered:
        create_table_artifact(
            table=filtered,
            key="filtered-exchangers",
            description="Отфильтрованные обменники (reserve > 10M, reviews > 5000)"
        )

    if len(filtered) >= 3:
        top10 = sorted(filtered, key=lambda x: x["rate"], reverse=True)[:10]

        names = [item["name"] for item in top10]
        rates = [item["rate"] for item in top10]

        plt.figure(figsize=(14, 8))
        plt.barh(names, rates, color="skyblue")
        plt.xlabel("Курс (RUB за 1 BTC)")
        plt.title(f"ТОП-10 обменников по курсу — {latest_timestamp}")
        plt.gca().invert_yaxis()
        plt.tight_layout()

        graph_file = f"{ARTIFACTS_DIR}/top10_rates_{now}.png"
        plt.savefig(graph_file, dpi=200, bbox_inches="tight")
        plt.close()

        try:
            from prefect.artifacts import create_image_artifact
            create_image_artifact(
                image_path=graph_file,
                description=f"ТОП-10 по курсу — {now}",
                key="top10-rate-chart"
            )
        except:
            pass

    print("Артефакты успешно созданы в Prefect UI")
    return count