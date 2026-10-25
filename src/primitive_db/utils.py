# для вспомогательных функций
import json


def load_metadata(filepath):  # для загрузки данных из JSON
    try:
        with open(filepath, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):  # сохраняет данные в JSON
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file)



