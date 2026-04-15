from prefect import flow, task
from scraper.scrape import scrape_bestchange
from scraper.analysis import run_analysis
from datetime import datetime, timedelta
import time

@task
def scrape_task():
    return scrape_bestchange()

@task
def analyze_task():
    return run_analysis()

@flow(name="BestChange Scraper - непрерывная версия")
def bestchange_flow(duration_hours: int = 24, scrape_interval_minutes: int = 30):
    print("Запускаю непрерывный процесс скрапинга BestChange...")

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=duration_hours)
    iteration = 0

    while datetime.now() < end_time:
        iteration += 1
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        remaining = (end_time - datetime.now()).total_seconds() / 60

        print(f"Итерация {iteration} | {current_time} | Осталось ≈ {int(remaining)} минут")

        scrape_task()
        analyze_task()

        if datetime.now() >= end_time:
            break

        time.sleep(scrape_interval_minutes * 60)

    total_hours = (datetime.now() - start_time).total_seconds() / 3600
    print(f"Процесс завершён. Работал {total_hours:.1f} часов.")
    print("Артефакты доступны в Prefect UI")