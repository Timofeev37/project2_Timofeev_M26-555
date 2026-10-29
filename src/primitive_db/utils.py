# для вспомогательных функций
import json
import os

from .constants import DATA_DIR


def load_metadata(filepath):
    """Загружает metadata из JSON-файла; если файла нет — возвращает {}."""
    try:
        with open(filepath, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет metadata в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file)


def load_table_data(table_name):
    """Загружает записи таблицы из data/<table_name>.json; если файла нет — []."""
    filepath = os.path.join(DATA_DIR, table_name + ".json")
    try:
        with open(filepath, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохраняет записи таблицы в data/<table_name>.json."""
    os.makedirs(DATA_DIR, exist_ok=True)  # создаёт папку, если её нет
    filepath = os.path.join(DATA_DIR, table_name + ".json")
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file)
