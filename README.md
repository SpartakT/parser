BestChange Scraper — BTC → Visa/Mastercard RUB

**Описание проекта**  

Это простой скрапер, который собирает актуальные курсы и информацию об обменниках с сайта BestChange (BTC → Visa/Mastercard RUB).  
Каждый запуск собирает все предложения, сохраняет их в файл и фильтрует по моим условиям:  
`reserve > 10 000 000 RUB` и `reviews > 5000`.

### Как запустить проект

```bash
Установка библиотек
pip install -r requirements.txt

python run.py all                  Рекомендуется: сбор данных + анализ + график
python run.py scrape               Только собрать свежие данные
python run.py analyze              Только анализ и построение графика

Непрерывный режим
python run.py continuous --hours 24 --interval 30