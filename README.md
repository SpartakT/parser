# BestChange Scraper — BTC → Visa/Mastercard RUB

**Описание проекта**  
Это простой скрапер, который собирает актуальные курсы и информацию об обменниках с сайта BestChange (BTC → Visa/Mastercard RUB).  
Каждый запуск собирает все предложения, сохраняет их в файл и фильтрует по моим условиям:  
`reserve > 10 000 000 RUB` и `reviews > 5000`.

### Как запустить проект

```bash
# Установка библиотек
pip install -r requirements.txt

# Основная команда (собрать данные + анализ)
python run.py all

# Другие команды:
python run.py scrape     # только собрать данные с сайта
python run.py analyze    # только выполнить анализ