# для работы с таблицами и данными

VALID_TYPES = {"int", "str", "bool"}


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