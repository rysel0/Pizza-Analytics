"""
Генерирует синтетические данные для пиццерии Arya's Pizza за неделю.
Имитирует выгрузку из POS-системы в CSV.
"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path
 
random.seed(42)  # для воспроизводимости
 
# --- Справочник блюд ---
MENU = [
    # (dish_id, dish_name, category, price, cost_price)
    (1, "Margherita", "Pizza", 550, 180),
    (2, "Pepperoni", "Pizza", 650, 220),
    (3, "Quattro Formaggi", "Pizza", 750, 290),
    (4, "Hawaiian", "Pizza", 680, 240),
    (5, "Meat Lovers", "Pizza", 820, 320),
    (6, "Vegetariana", "Pizza", 620, 210),
    (7, "Caesar Salad", "Salad", 420, 150),
    (8, "Greek Salad", "Salad", 380, 120),
    (9, "Tuna Salad", "Salad", 460, 180),
    (10, "Carbonara", "Pasta", 480, 170),
    (11, "Bolognese", "Pasta", 460, 160),
    (12, "Seafood Pasta", "Pasta", 620, 280),
    (13, "Coca-Cola 0.5", "Drinks", 150, 45),
    (14, "Lemonade", "Drinks", 180, 40),
    (15, "Black Tea", "Drinks", 90, 15),
    (16, "Cappuccino", "Drinks", 220, 55),
    (17, "Tiramisu", "Dessert", 290, 95),
    (18, "Cheesecake", "Dessert", 320, 110),
    (19, "Panna Cotta", "Dessert", 270, 85),
    (20, "Minestrone Soup", "Soup", 350, 120),
    (21, "Mushroom Cream Soup", "Soup", 380, 140),
    # Намеренно добавим пару позиций с плохой маржой
    (22, "Caviar Bruschetta", "Appetizer", 450, 400),
    (23, "Premium Antipasto", "Appetizer", 890, 750),
]
 
# --- Веса популярности блюд ---
POPULARITY_WEIGHTS = {
    1: 30, 2: 28, 3: 20, 4: 18, 5: 15, 6: 12,   # пиццы
    7: 15, 8: 12, 9: 8,                          # салаты
    10: 14, 11: 12, 12: 6,                       # паста
    13: 35, 14: 25, 15: 40, 16: 20,              # напитки
    17: 10, 18: 12, 19: 6,                       # десерты
    20: 5, 21: 4,                                # супы
    22: 2, 23: 1,                                # дорогие закуски
}
 
 
def get_hour_weight(hour: int) -> float:
    """Моделируем загруженность по часам: обед и вечер — пик."""
    if 12 <= hour <= 14:
        return 3.0
    if 18 <= hour <= 22:
        return 4.0
    if 15 <= hour <= 17:
        return 1.2
    if 10 <= hour <= 11:
        return 0.8
    return 0.3
 
 
def generate():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
 
    # --- 1. menu.csv ---
    with open(data_dir / "menu.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dish_id", "dish_name", "category", "price", "cost_price"])
        for row in MENU:
            w.writerow(row)
    print(f"✓ menu.csv — {len(MENU)} dishes")
 
    # --- 2 и 3. orders.csv и order_items.csv ---
    orders = []
    order_items = []
    order_id = 1000
 
    start_date = datetime(2026, 4, 13, 10, 0, 0)  # понедельник
    dish_ids = [m[0] for m in MENU]
    dish_weights = [POPULARITY_WEIGHTS[d] for d in dish_ids]
    menu_prices = {m[0]: m[3] for m in MENU}
 
    for day in range(7):
        for hour in range(10, 24):
            weight = get_hour_weight(hour)
            n_orders_this_hour = max(0, int(random.gauss(5 * weight, 2)))
 
            for _ in range(n_orders_this_hour):
                order_id += 1
                minute = random.randint(0, 59)
                dt = start_date + timedelta(days=day, hours=hour - 10, minutes=minute)
 
                table = random.randint(1, 15)
                waiter = random.randint(1, 5)
 
                n_items = random.choices([1, 2, 3, 4, 5], weights=[15, 35, 30, 15, 5])[0]
                chosen_dishes = random.choices(dish_ids, weights=dish_weights, k=n_items)
 
                total = 0
                for dish_id in set(chosen_dishes):
                    quantity = chosen_dishes.count(dish_id)
                    price = menu_prices[dish_id]
                    line_total = quantity * price
                    total += line_total
                    order_items.append({
                        "order_id": order_id,
                        "dish_id": dish_id,
                        "quantity": quantity,
                        "item_price": price,
                    })
 
                orders.append({
                    "order_id": order_id,
                    "order_datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "table_number": table,
                    "waiter_id": waiter,
                    "total_amount": total,
                })
 
    with open(data_dir / "orders.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["order_id", "order_datetime", "table_number", "waiter_id", "total_amount"])
        w.writeheader()
        w.writerows(orders)
    print(f"✓ orders.csv — {len(orders)} orders")
 
    with open(data_dir / "order_items.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["order_id", "dish_id", "quantity", "item_price"])
        w.writeheader()
        w.writerows(order_items)
    print(f"✓ order_items.csv — {len(order_items)} items")
 
 
if __name__ == "__main__":
    generate()