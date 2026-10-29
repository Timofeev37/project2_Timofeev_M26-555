# парсеры для where/set-условий и значений команд


def parse_value(raw_value):
    """Приводит строковый токен к int/bool, иначе оставляет как str."""
    if raw_value == "true":  # отдельно для True/False
        return True
    if raw_value == "false":
        return False
    try:
        return int(raw_value)  # поддерживаемые типы: int, str, bool
    except ValueError:
        return raw_value


def parse_condition(tokens):
    """Превращает токены вида ['age', '=', '28'] в {'age': 28}."""
    column, _, raw_value = tokens
    return {column: parse_value(raw_value)}
