import streamlit as st
import json
import time
import uuid
from pathlib import Path

st.set_page_config(
    page_title="Shop Inventory Portal",
    page_icon=" ",
    layout="centered",
    initial_sidebar_state="expanded",
)

inventory_file = Path("inventory.json")
sales_file = Path("sales.json")
users_file = Path("users.json")

def save_inventory():
    with open(inventory_file, "w", encoding="utf-8") as f:
        json.dump(st.session_state["inventory"], f, indent=2)

def save_sales():
    with open(sales_file, "w", encoding="utf-8") as f:
        json.dump(st.session_state["sales"], f, indent=2)

def save_users():
    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(st.session_state["users"], f, indent=2)

#Inventory

def load_inventory():
    default = [
        {"item_id": 1, "name": "Sourdough Loaf",   "price": 8.50, "stock": 12, "category": "Bread",   "flagged": False},
        {"item_id": 2, "name": "Croissant",         "price": 3.25, "stock": 20, "category": "Pastry",  "flagged": False},
        {"item_id": 3, "name": "Blueberry Muffin",  "price": 2.95, "stock": 4,  "category": "Pastry",  "flagged": False},
        {"item_id": 4, "name": "Cinnamon Roll",     "price": 4.00, "stock": 8,  "category": "Pastry",  "flagged": False},
        {"item_id": 5, "name": "Whole Wheat Loaf",  "price": 7.75, "stock": 6,  "category": "Bread",   "flagged": False},
        {"item_id": 6, "name": "Chocolate Eclair",  "price": 4.50, "stock": 3,  "category": "Pastry",  "flagged": False},
        {"item_id": 7, "name": "Bagel",             "price": 2.00, "stock": 15, "category": "Bread",   "flagged": False},
        {"item_id": 8, "name": "Lemon Tart",        "price": 5.25, "stock": 2,  "category": "Dessert", "flagged": False},
    ]
    if inventory_file.exists():
        with open(inventory_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return default

        next_id = max(
            (item.get("item_id") or item.get("id") or 0)
            for item in data if isinstance(item, dict)
        ) + 1
        changed = False

        for item in data:
            if not isinstance(item, dict):
                continue

            if "item_id" not in item:
                if "id" in item:
                    item["item_id"] = item.pop("id")
                else:
                    item["item_id"] = next_id
                    next_id += 1
                changed = True

            if "category" not in item:
                item["category"] = "Other"
                changed = True

            if "flagged" not in item:
                item["flagged"] = False
                changed = True

        if changed:
            with open(inventory_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

        return data

    with open(inventory_file, "w", encoding="utf-8") as f:
        json.dump(default, f, indent=2)
    return default

def load_sales():
    if sales_file.exists():
        with open(sales_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def load_users():
    default = [
        {"username": "owner",    "password": "owner123",    "role": "Owner"},
        {"username": "employee", "password": "employee123", "role": "Employee"},
    ]
    if users_file.exists():
        with open(users_file, "r", encoding="utf-8") as f:
            return json.load(f)
    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(default, f, indent=2)
    return default