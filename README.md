# Arya's Pizza Analytics
 
DWH для пиццерии Arya's Pizza. Отвечает на вопросы:
- Какие блюда приносят больше всего выручки?
- Какие блюда убыточны (маржа < 20%)?
- Когда пиковая нагрузка?
 
## Запуск
 
1. `python3 -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. `python generate_data.py` - сгенерировать тестовые данные
4. `docker compose up -d` - поднять ClickHouse
5. `python load_csv.py` - загрузить данные в raw-слой
6. `cd aryas_dbt && dbt build` - построить staging и marts
 
## Остановка
 
- Остановить ClickHouse: `docker compose stop`
- Удалить контейнер (данные сохранятся): `docker compose down`
- Полный сброс: `docker compose down -v && rm -rf clickhouse_data/`