from fastapi import HTTPException
from typing import List, Dict
from pathlib import Path
from threading import Lock
import json
from copy import deepcopy

file_lock = Lock()
DATA_FILE = Path(__file__).parent.parent/"data"/"products.json"

print(DATA_FILE)
file_lock = Lock()

def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        raise HTTPException(status_code=404, detail="File data not found.")
    with file_lock:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)




# List all products
def get_all_products() -> List[Dict]:
    return load_products()

#Save Products
def save_products(products):
    with file_lock:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(products, f, indent=2)



# Add Products
def add_product_to_store(product: Dict) -> Dict:
    products = get_all_products()
    if any(p["sku"] == product["sku"] for p in products):
        raise ValueError("SKU Code already exists")
    products.append(product)
    save_products(products)
    return product


# Delete Products
def remove_products(id: str) -> str:
    products = get_all_products()
    for idx, p in enumerate(products):
        if p["id"] == str(id):
            deleted = products.pop(idx)
            save_products(products)
            return {"message" : "Product deleted successfully", "data": deleted}


# Update Products


def change_product(product_id: str, update_data: dict) -> dict:
    products = get_all_products()
    for idx, original in enumerate(products):
        if original["id"] == product_id:
            updated = deepcopy(original)

            for key, value in update_data.items():
                if value is None:
                    continue

                # Merge dicts if needed
                if isinstance(value, dict) and isinstance(updated.get(key), dict):
                    updated[key].update(value)
                else:
                    updated[key] = value

            products[idx] = updated
            save_products(products)
            return updated

    raise HTTPException(status_code=404, detail="Product not found")

