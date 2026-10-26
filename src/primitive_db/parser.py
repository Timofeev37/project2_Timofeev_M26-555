# парсеры для where/set-условий и значений команд

import ast


def parse_value(raw_value):  # обработка вводимых значений
    if raw_value == "true": # отдельно для True/False
        return True
    if raw_value == "false":
        return False
    try:
        return ast.literal_eval(raw_value) #для остальных через библиотеку ast
    except (ValueError, SyntaxError):
        return raw_value


def parse_condition(tokens):  # расшивка аргументов
    column, _, raw_value = tokens
    return {column: parse_value(raw_value)}

