import shlex

import prompt

from .core import create_table, drop_table
from .utils import load_metadata, save_metadata


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    command_list = ["help", "exit", "create_table", "drop_table", "list_tables"]

    print('Первая попытка запустить проект!')
    print('Загрузка таблиц...')
    filepath = 'db_metadata.json'
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

if __name__ == '__main__':
    run()

