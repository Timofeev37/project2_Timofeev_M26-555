import functools
import time

from .constants import CONFIRMABLE_ACTIONS


def handle_db_errors(func):
    """Декоратор: перехватывает ошибки БД и печатает понятное сообщение."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper

def confirm_action(action_name):
    """Фабрика декораторов: перед вызовом функции спрашивает подтверждение."""

    def decorator(func):
        """Оборачивает func запросом 'y/n' в консоли."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if action_name in CONFIRMABLE_ACTIONS:
                prompt_text = f'Вы уверены, что хотите выполнить {action_name} (y/n)?'
                if input(prompt_text) == 'y':
                    return func(*args, **kwargs)
                else:
                    print('Операция отменена')
        return wrapper
    return decorator

def log_time(func):
    """Декоратор: замеряет и печатает время выполнения func."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func_name = func.__name__
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'Время выполнения функции {func_name}: {end_time - start_time} сек.')
        return result
    return wrapper

def create_cacher():
    """Создаёт изолированный кэш и возвращает (cache_result, invalidate)."""
    cache = {}

    def cache_result(key, value_func):
        """Отдаёт закэшированное значение по key либо считает и кэширует его."""
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result

    def invalidate(table_name):
        """Удаляет из кэша все записи, относящиеся к table_name."""
        stale_keys = [key for key in cache if key[0] == table_name]
        for key in stale_keys:
            del cache[key]

    return cache_result, invalidate
