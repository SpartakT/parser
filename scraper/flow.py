from prefect import flow, task
from scraper.scrape import scrape_bestchange
from scraper.analysis import run_analysis

@task
def scrape_task():
    return scrape_bestchange()

@task
def analyze_task():
    return run_analysis()

@flow(name="BestChange Scraper - простая версия")
def bestchange_flow():
    print("Запускаю весь процесс скрапера...")
    scrape_task()
    analyze_task()
    print("Процесс завершён! Данные в data/raw_data.txt и artifacts/")