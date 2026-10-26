# для работы с таблицами и данными
from .utils import load_table_data, save_table_data


VALID_TYPES = {"int", "str", "bool"}

type_mapping = {
    "int": int,
    "str": str,
    "bool": bool}

def create_table(metadata, table_name, columns):  # создание таблицы
    if table_name in metadata: #проверка существования таблицы
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = {"ID": "int"}
    for column in columns:
        # partition устойчив к пустому/лишнему ":" в отличие от split
        column_name, _, column_type = column.partition(":")
        if column_type not in VALID_TYPES: #проверка типов данных для столбцов
            print(f"Некорректное значение: {column_type}. Попробуйте снова.")
            return metadata
        table_columns[column_name] = column_type

    metadata[table_name] = table_columns #запись новой таблицы в metadata
    columns_str = ", ".join(
        f"{name}:{col_type}" for name, col_type in table_columns.items()
    )
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')
    return metadata


def drop_table(metadata, table_name):  # удаление таблицы
    if table_name not in metadata: #проверка существования таблицы
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

def insert(metadata, table_name, values):  # создание записи
    if table_name not in metadata:  # проверка существования таблицы
        print(f'Ошибка: Таблицы "{table_name}" не существует.')
        return None

    columns = list(metadata[table_name].keys())[1:]  # без ID
    if len(values) != len(columns): # проверяем количество значений в таблице и значений values
        print(
            f'Ошибка: таблица "{table_name}" ожидает {len(columns)} '
            f"значений, получено {len(values)}."
        )
        return None

    types = [type_mapping[metadata[table_name][column]] for column in columns] # получаем необходимые типы данных
    if not all(isinstance(value, expected) for value, expected in zip(values, types)): # проверяем совпадение типов
        print("Ошибка: неверный тип одного из значений.")
        return None

    data = load_table_data(table_name) #загружаем данные таблицы
    new_id = max((record["ID"] for record in data), default=0) + 1 #получаем акутальный ID

    record = {"ID": new_id} # назначаем ID
    record.update(zip(columns, values)) # обновляем пары ключ-значение для заполнения в таблицу
    data.append(record) # добавляем в данные для записи

    save_table_data(table_name, data) # сохраняем в таблицу
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return data


def select(table_data, where_clause=None):  # чтение записей
    if where_clause is None:
        return table_data

    return [
        record
        for record in table_data
        if all(record.get(column) == value for column, value in where_clause.items())
    ] # генераторный список, проверяющий каждую запись на соответствие условию where_clause

def update(table_data, set_clause, where_clause): # обновление записей в таблице
    if where_clause is None:
        return table_data

    updated_data = []
    for record in table_data: # для каждой записи проверяем соответствие условию where_clause
        if all(record.get(column) == value for column, value in where_clause.items()):
            record.update(set_clause) #обновляем в соответствии set_clause
        updated_data.append(record)
    return updated_data


def delete(table_data, where_clause): # удаление записей из таблицы
    if where_clause is None:
        return table_data
    updated_data = table_data.copy()
    for record in table_data: # для каждой записи проверяем соответствие условию where_clause
        if all(record.get(column) == value for column, value in where_clause.items()):
            updated_data.remove(record) # удаляем соответствующие

    return updated_data

