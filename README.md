# BestChange Scraper — BTC → Visa/Mastercard RUB

Скрапер собирает актуальные курсы обмена **Bitcoin → Visa/Mastercard RUB** с сайта BestChange.net.

Каждый запуск сохраняет данные в `data/raw_data.txt`, фильтрует надёжные обменники, строит графики ТОП-10 по курсу и другим параметрам и сохраняет их в artifacts/

## Как запустить проект

```bash
# 1. Установка зависимостей
pip install -r requirements.txt
```

## Основные команды

```bash
python run.py all        # сбор + анализ + график
python run.py scrape     # только сбор данных
python run.py analyze    # только анализ и график
```

## Непрерывный режим

```bash
python run.py continuous --hours 24 --interval 30
```

## Примеры использования

```bash
python run.py all
python run.py continuous --hours 12 --interval 20
```

## Запуск через Prefect

```bash
prefect server start    # в отдельном терминале
prefect deploy -n bestchange-every-hour
```

## Где смотреть результаты

* Сырые данные: `data/raw_data.txt`
* Графики и отчёты: `artifacts/`
* Prefect UI: http://127.0.0.1:4200
