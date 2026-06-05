import json
import os

WAREHOUSE_FILE = "warehouse.json"
HISTORY_FILE = "history.json"


def load_warehouse():
    if not os.path.exists(WAREHOUSE_FILE):
        return {}

    with open(WAREHOUSE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_warehouse(data):
    with open(WAREHOUSE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def add_history_entry(entry):
    history = load_history()
    history.append(entry)
    save_history(history)
