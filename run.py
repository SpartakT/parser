import argparse
from scraper.scrape import scrape_bestchange
from scraper.analysis import run_analysis


def main():
    parser = argparse.ArgumentParser(
        description="BestChange Scraper — BTC → Visa/Mastercard RUB"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scrape_parser = subparsers.add_parser("scrape", help="Только собрать данные с сайта")
    analyze_parser = subparsers.add_parser("analyze", help="Только выполнить анализ")
    all_parser = subparsers.add_parser("all", help="Собрать данные + сразу сделать анализ")

    # Добавляем аргументы для непрерывного режима (опционально)
    continuous_parser = subparsers.add_parser(
        "continuous",
        help="Запустить непрерывный процесс на указанное время"
    )
    continuous_parser.add_argument(
        "--hours", type=int, default=24,
        help="Сколько часов работать (по умолчанию 24)"
    )
    continuous_parser.add_argument(
        "--interval", type=int, default=30,
        help="Интервал между скрапингами в минутах (по умолчанию 30)"
    )

    args = parser.parse_args()

    print("BestChange Scraper — BTC → Visa/Mastercard RUB")

    if args.command in ["scrape", "all"]:
        print("Запускаю сбор данных с BestChange")
        scrape_bestchange()

    if args.command in ["analyze", "all"]:
        print("Запускаю анализ и создание артефактов...")
        run_analysis()

    if args.command == "continuous":
        from scraper.flow import bestchange_flow
        print(f"Запускаю непрерывный режим на {args.hours} часов (интервал {args.interval} мин)...")
        bestchange_flow(duration_hours=args.hours, scrape_interval_minutes=args.interval)

    print("Готово!")
    print("Данные хранятся в:          data/raw_data.txt")
    print("Артефакты и графики:       artifacts/")


if __name__ == "__main__":
    main()