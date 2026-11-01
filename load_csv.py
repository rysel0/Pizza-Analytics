"""
Загрузка CSV в ClickHouse через HTTP-интерфейс.
Перед загрузкой делаем TRUNCATE, чтобы повторный запуск не дублировал данные.
"""
import requests
from pathlib import Path
import time
 
CLICKHOUSE_URL = "http://localhost:8123"
AUTH = ("analyst", "analyst123")
 
 
def execute(query: str) -> str:
    response = requests.post(CLICKHOUSE_URL, params={"query": query}, auth=AUTH)
    response.raise_for_status()
    return response.text
 
 
def truncate_table(table: str):
    execute(f"TRUNCATE TABLE {table}")
    print(f"  TRUNCATE {table}")
 
 
def load_csv(table: str, csv_path: Path):
    query = f"INSERT INTO {table} FORMAT CSVWithNames"
    with open(csv_path, "rb") as f:
        response = requests.post(
            CLICKHOUSE_URL,
            params={"query": query},
            data=f,
            auth=AUTH,
        )
    response.raise_for_status()
 
    count = execute(f"SELECT count() FROM {table}").strip()
    print(f"  ✓ {table} ← {csv_path}  ({count} rows)")
 
 
def main():
    data_dir = Path("data")
    tables = [
        ("raw.menu", data_dir / "menu.csv"),
        ("raw.orders", data_dir / "orders.csv"),
        ("raw.order_items", data_dir / "order_items.csv"),
    ]
 
    print("Loading CSVs into ClickHouse:")
    for table, path in tables:
        truncate_table(table)
        load_csv(table, path)
        # time.sleep(1)
    print("Done.")
 
 
if __name__ == "__main__":
    main()