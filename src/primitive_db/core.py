# для работы с таблицами и данными
from .constants import TYPE_MAPPING, VALID_TYPES
from .decorators import confirm_action, create_cacher, handle_db_errors, log_time
from .utils import load_table_data, save_table_data

_cache_select, invalidate_select_cache = create_cacher()

@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создаёт таблицу table_name со столбцами columns (+ автo ID:int)."""
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

@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata, table_name):
    """Удаляет таблицу table_name из metadata (с подтверждением)."""
    if table_name not in metadata: #проверка существования таблицы
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """Добавляет запись values в table_name с автогенерацией ID."""
    if table_name not in metadata:  # проверка существования таблицы
        print(f'Ошибка: Таблицы "{table_name}" не существует.')
        return None

    columns = list(metadata[table_name].keys())[1:]  # без ID
    if len(values) != len(columns):  # сверяем кол-во значений и столбцов
        print(
            f'Ошибка: таблица "{table_name}" ожидает {len(columns)} '
            f"значений, получено {len(values)}."
        )
        return None

    # нужные типы для проверки
    types = [TYPE_MAPPING[metadata[table_name][column]] for column in columns]
    if not all(isinstance(value, expected) for value, expected in zip(values, types)):
        print("Ошибка: неверный тип одного из значений.")
        return None

    data = load_table_data(table_name)  # загружаем данные таблицы
    new_id = max((record["ID"] for record in data), default=0) + 1  # новый ID

    record = {"ID": new_id}  # назначаем ID
    record.update(zip(columns, values))  # заполняем остальные поля
    data.append(record)  # добавляем в данные для записи

    save_table_data(table_name, data) # сохраняем в таблицу
    invalidate_select_cache(table_name)  # старые закэшированные select устарели
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return data


@handle_db_errors
@log_time
def select(table_data, where_clause=None, table_name=None):
    """Возвращает записи table_data, подходящие под where_clause (с кэшем)."""
    def compute():
        """Реально вычисляет отфильтрованный результат (для кэша)."""
        if where_clause is None:
            return table_data
        return [
            record
            for record in table_data
            if all(
                record.get(column) == value
                for column, value in where_clause.items()
            )
        ]

    if table_name is None:  # без имени таблицы кэшировать небезопасно
        return compute()

    cache_key = (table_name, frozenset(where_clause.items()) if where_clause else None)
    return _cache_select(cache_key, compute)

@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Обновляет записи, подходящие под where_clause, согласно set_clause."""
    if where_clause is None:
        return table_data

    updated_data = []
    ids = []
    for record in table_data:  # проверяем соответствие условию where_clause
        if all(record.get(column) == value for column, value in where_clause.items()):

            record.update(set_clause)  # обновляем в соответствии с set_clause

            ids.append(record.get("ID"))
            updated_data.append(record)
        else:
            updated_data.append(record)
    return ids, updated_data

@confirm_action("удаление строки")
@handle_db_errors
def delete(table_data, where_clause):
    """Удаляет записи, подходящие под where_clause (с подтверждением)."""
    if where_clause is None:
        return table_data
    updated_data = table_data.copy()
    ids = []
    for record in table_data:  # проверяем соответствие условию where_clause
        if all(record.get(column) == value for column, value in where_clause.items()):
            ids.append(record.get("ID"))
            updated_data.remove(record)  # удаляем соответствующие

    return ids, updated_data

