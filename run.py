import argparse
from scraper.scrape import scrape_bestchange
from scraper.analysis import run_analysis


def main():
    parser = argparse.ArgumentParser(
        description="Скрапер BestChange BTC → Visa/Mastercard RUB"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    scrape_parser = subparsers.add_parser("scrape", help="Только собрать данные с сайта")
    analyze_parser = subparsers.add_parser("analyze", help="Только запустить анализ и создать отфильтрованный файл")
    all_parser = subparsers.add_parser("all", help="Собрать данные + сразу сделать анализ")
    args = parser.parse_args()

    print("=" * 65)
    print("BestChange Scraper (CLI с subparsers)")
    print("=" * 65)

    if args.command == "scrape" or args.command == "all":
        print("Запускаю сбор данных с BestChange...")
        scrape_bestchange()
        print("-" * 50)

    if args.command == "analyze" or args.command == "all":
        print("Запускаю анализ и фильтрацию...")
        run_analysis()
        print("-" * 50)

    print("Всё выполнено!")
    print("Данные: data/raw_data.txt")
    print("Результаты: папка artifacts/")


if __name__ == "__main__":
    main()