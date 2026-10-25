import prompt


def main():
    print('Первая попытка запустить проект!')
    while True:
        message = '''
        <command> help - справочная информация
        <command> exit - выход из программы
        '''
        print(message)
        command = prompt.string('Введите команду:')
        if command == 'help':
            print(message)
        elif command == 'exit':
            break

if __name__ == '__main__':
    main()

