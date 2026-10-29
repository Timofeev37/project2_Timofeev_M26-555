#!/usr/bin/env python3

from . import engine


def main():
    """Точка входа приложения: запускает основной цикл engine.run()."""
    print("DB project is running!")
    engine.run()
if __name__ == "__main__":
    main()
