import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from prefect import task, flow
from prefect.artifacts import create_markdown_artifact

DATA_DIR = "data"
ARTIFACTS_DIR = "artifacts"

if not os.path.exists(ARTIFACTS_DIR):
    os.makedirs(ARTIFACTS_DIR)

RAW_TXT = os.path.join(DATA_DIR, "raw_data.txt")


@task
def analyze_data():
    if not os.path.exists(RAW_TXT):
        print("Нет файла raw_data.txt")
        return

    with open(RAW_TXT, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"Анализ данных на момент: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    filtered = []
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 5:
            continue

        try:
            reserve = int(parts[3])
            reviews = int(parts[4])
            rate = float(parts[2])

            # Смягчённый фильтр
            if reserve > 500_000 and reviews > 50:
                filtered.append({
                    "name": parts[1],
                    "rate": rate,
                    "reserve": reserve,
                    "reviews": reviews,
                    "min_btc": parts[5] if len(parts) > 5 else "",
                    "max_btc": parts[6] if len(parts) > 6 else ""
                })
        except (ValueError, IndexError):
            continue

    print(f"Под фильтр подошло {len(filtered)} обменников")

    if not filtered:
        print("Нет данных для анализа.")
        return

    df = pd.DataFrame(filtered)

    # Сохраняем CSV
    csv_path = os.path.join(ARTIFACTS_DIR, "bestchange_top.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")

    # График
    plt.figure(figsize=(12, 6))
    top10 = df.nlargest(10, 'reserve')
    plt.barh(top10['name'], top10['reserve'])
    plt.xlabel('Резерв (RUB)')
    plt.ylabel('Обменник')
    plt.title('Топ-10 обменников по резерву')
    plt.tight_layout()
    plt.savefig(os.path.join(ARTIFACTS_DIR, "top_reserve.png"))
    plt.close()

    # Markdown artifact
    markdown = f"""
# Результаты анализа BestChange

**Время анализа:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Найдено обменников после фильтра:** {len(df)}

## Топ по резерву
{df.nlargest(10, 'reserve')[['name', 'rate', 'reserve', 'reviews']].to_markdown(index=False)}
    """

    create_markdown_artifact(
        key="bestchange-analysis",
        markdown=markdown,
        description="Результаты парсинга BestChange"
    )

    print("Артефакты успешно созданы в Prefect UI")


@flow
def analysis_flow():
    analyze_data()


if __name__ == "__main__":
    analysis_flow()