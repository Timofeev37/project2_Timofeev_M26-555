import shlex

import prompt

from .core import create_table, drop_table, insert, select, update, delete
from .utils import load_metadata, save_metadata, load_table_data, save_table_data

from .parser import parse_value, parse_condition

from pathlib import Path
from prettytable import PrettyTable


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\n***Процесс работы с дыннами***")
    print("Функции:")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.")
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    command_list = ["help", "exit", "create_table", "drop_table", "list_tables", "insert", "select", "update", "delete", "info"]

    print('Первая попытка запустить проект!')
    print('Загрузка таблиц...')

    filepath = Path(__file__).parent / 'db_metadata.json'
    metadata = load_metadata(filepath)
    print_help()
    while True:


        command_string = prompt.string('Введите команду:')
        args = shlex.split(command_string)
        command = args[0]
        if command not in command_list:
            print(f'Функции {command} нет. Попробуйте еще раз')
            continue
        match command:
            case 'help':
                print_help()
            case 'exit':
                break
            case 'create_table':
                try:
                    table = args[1]
                    columns = args[2:]
                    metadata = create_table(metadata,table,columns)
                    save_metadata(filepath, metadata)
                except IndexError:
                    print('Неправильный формат команды')
                    continue

            case 'drop_table':
                try:
                    if len(args) > 2:
                        raise IndexError
                    table = args[1]
                    metadata = drop_table(metadata,table)
                    save_metadata(filepath, metadata)
                except IndexError:
                    print('Неправильный формат команды')
                    continue

            case 'list_tables':
                if metadata:
                    for tables in metadata.keys():
                        print(f'-   {tables}')
                else:
                    print ('Таблиц нет')


            case 'insert':
                try:
                    table = args[2]
                    # снимаем скобки "(" ")" и запятые, которые shlex не режет
                    # как отдельные разделители (например, токен "28,")
                    values_raw = [token.strip('(),') for token in args[4:]]
                    values_raw = [token for token in values_raw if token]
                    values = []
                    try:
                        for value in values_raw:
                            values.append( parse_value(value))
                    except ValueError:
                        print('Ошибка при вводе значений!')
                        continue
                    print(values)
                    insert(metadata,table,values)
                except IndexError:
                    print('Неправильный формат команды')
                    continue

            case 'select':
                try:
                    if args[1] != 'from':
                        raise IndexError
                    table = args[2]
                except IndexError:
                    print('Неправильный формат команды')
                    continue

                if table not in metadata:  # проверка существования таблицы
                    print(f'Ошибка: Таблицы "{table}" не существует.')
                    continue

                clause_tokens = args[4:]  # то, что после слова "where"
                where_clause = None
                if clause_tokens:
                    try:
                        where_clause = parse_condition(clause_tokens)
                    except ValueError:
                        print('Можно задать только 1 условие!')
                        continue

                table_data = load_table_data(table)  # загружаем данные таблицы
                result = select(table_data, where_clause=where_clause)

                columns = list(metadata[table].keys())
                pretty = PrettyTable()
                pretty.field_names = columns
                for record in result:
                    pretty.add_row([record[column] for column in columns])
                print(pretty)

            case 'update':
                try:
                    table = args[1]
                except IndexError:
                    print('Неправильный формат команды')
                    continue

                if table not in metadata:  # проверка существования таблицы
                    print(f'Ошибка: Таблицы "{table}" не существует.')
                    continue

                try:
                    set_clause = parse_condition(args[3:6])
                except ValueError:
                    print('Ошибка в указании обновленных данных')
                    continue
                try:
                    where_clause = parse_condition(args[7:])
                except ValueError:
                    print('Ошибка в указании условий обновления')
                    continue

                table_data = load_table_data(table)  # загружаем данные таблицы
                ids, table_data = update(table_data, set_clause, where_clause)
                if not ids:
                    print('Ни одной записи не обновлено')
                elif len(ids) == 1:
                    print(f'Запись с ID={ids[0]} успешно обновлена')
                else:
                    print(f'Записи с ID=',end='')
                    for i, id in enumerate(ids):
                        print(f'{id}' if i == 0 else f', {id}', end='')
                    print(' успешно обновлены')
                save_table_data(table,table_data)

            case 'delete':
                try:
                    table = args[2]
                except IndexError:
                    print('Неправильный формат команды')
                    continue

                if table not in metadata:  # проверка существования таблицы
                    print(f'Ошибка: Таблицы "{table}" не существует.')
                    continue

                clause_raw = args[4:]
                try:
                    clause = parse_condition(clause_raw)
                except ValueError:
                    print('Можно задать только 1 условие!')
                    continue

                table_data = load_table_data(table)
                ids, table_data = delete(table_data, clause)
                if not ids:
                    print('Ни одна запись не была удалена')
                elif len(ids) == 1:
                    print(f'Запись с ID={ids[0]} успешно удалена')
                else:
                    print(f'Записи с ID=',end='')
                    for i,id in enumerate(ids):
                        print(f'{id}'if i==0 else f', {id}',end='')
                    print(' успешно удалены')
                save_table_data(table,table_data)

            case 'info':
                try:
                    table = args[1]
                except IndexError:
                    print('Неправильный формат команды')
                    continue
                if table not in metadata:  # проверка существования таблицы
                    print(f'Ошибка: Таблицы "{table}" не существует.')
                    continue
                table_data = load_table_data(table)
                table_columns = metadata[table]  # запись новой таблицы в metadata
                columns_str = ", ".join(
                    f"{name}:{col_type}" for name, col_type in table_columns.items()
                )
                print(f'Таблица: "{table}')
                print(f'Столбцы: {columns_str}')
                print(f'Количество записей: {len(table_data)}')

if __name__ == '__main__':
    run()

