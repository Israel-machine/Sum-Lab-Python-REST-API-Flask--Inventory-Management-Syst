import json
import os
from lib.data import products

DB_PATH = "data/db.json"

def save_data():
    """Writes the current products list to a JSON file."""
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        with open(DB_PATH, "w") as f:
            json.dump(products, f, indent=4)
        print("Data successfully saved to db.json")
    except Exception as e:
        print(f"Error saving data: {e}")

def load_data():
    """Loads products from the JSON file into the products list on startup."""
    if not os.path.exists(DB_PATH):
        return

    try:
        with open(DB_PATH, "r") as f:
            content = f.read()
            if content:
                loaded_products = json.loads(content)
                products.clear()
                products.extend(loaded_products)
    except Exception as e:
        print(f"Error loading data: {e}")