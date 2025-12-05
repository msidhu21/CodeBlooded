import os
import csv
from pathlib import Path

# Get absolute path to backend/data/cart.csv
BASE_DIR = Path(__file__).resolve().parent.parent.parent   # backend/
DATA_DIR = BASE_DIR / "data"
CART_FILE = DATA_DIR / "cart.csv"

class CartRepo:

    @staticmethod
    def add_item(user_id: str, product_id: str, quantity: int = 1):
        # Ensure file exists and has header row
        if not CART_FILE.exists():
            with open(CART_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["user_id", "product_id", "quantity"])

        with open(CART_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([user_id, product_id, quantity])

    @staticmethod
    def get_items(user_id: str):
        if not CART_FILE.exists():
            return []

        items = []
        with open(CART_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["user_id"] == user_id:
                    items.append({
                        "user_id": row["user_id"],
                        "product_id": row["product_id"],
                        "quantity": int(row["quantity"])
                    })
        return items

    @staticmethod
    def remove_item(user_id: str, product_id: str):
        if not CART_FILE.exists():
            return

        rows = []
        with open(CART_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not (row["user_id"] == user_id and row["product_id"] == product_id):
                    rows.append(row)

        # Rewrite file with header
        with open(CART_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["user_id", "product_id", "quantity"])
            writer.writeheader()
            writer.writerows(rows)

