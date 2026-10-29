# именованные константы проекта, чтобы не разбрасывать магические значения по коду

META_FILE = "db_metadata.json"
DATA_DIR = "data"

VALID_TYPES = {"int", "str", "bool"}
TYPE_MAPPING = {
    "int": int,
    "str": str,
    "bool": bool,
}

CONFIRMABLE_ACTIONS = ["удаление строки", "удаление таблицы"]

COMMANDS = [
    "help", "exit", "create_table", "drop_table", "list_tables",
    "insert", "select", "update", "delete", "info",
]
