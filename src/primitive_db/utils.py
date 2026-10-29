# для вспомогательных функций
import json
from pathlib import Path


def load_metadata(filepath):  # для загрузки данных из JSON
    try:
        with open(filepath, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):  # сохраняет данные в JSON
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file)

def load_table_data(table_name):   # для загрузки данных таблицы из JSON
    BASE_DIR = Path(__file__).parent  # папка, где лежит utils.py
    DATA_DIR = BASE_DIR / "data"
    filename = table_name + '.json'
    filepath = DATA_DIR / filename
    try:
        with open(filepath, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_table_data(table_name, data):    # для сохранения данных таблицы в JSON
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    DATA_DIR.mkdir(exist_ok=True)  # ← создаёт папку, если её нет
    filename = table_name + '.json'
    filepath = DATA_DIR / filename
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file)




