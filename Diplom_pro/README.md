# Тестовый проект: Автоматизация тестирования веб-приложения (UI + API)

Проект автоматизации тестирования веб-приложения, включающий UI-тесты на Selenium и API-тесты на Python.

## Структура проекта
Diplom_pro/
│
├── 📁 pages/                  # Page Object модели
│   ├── __init__.py           # Пакет pages
│   ├── base_page.py          # Базовый класс с общими методами
│   ├── main_page.py          # Главная страница
│   ├── search_page.py        # Страница поиска
│   ├── product_page.py       # Страница товара
│   └── cart_page.py          # Страница корзины
│
├── 📁 tests/                  # Тестовые сценарии
│   ├── __init__.py           # Пакет tests
│   ├── conftest.py           # Фикстуры pytest
│   ├── test_smoke.py         # Smoke-тесты
│   ├── test_ui.py            # UI-тесты
│   └── test_api.py           # API-тесты
│
├── 📁 utils/                  # Вспомогательные утилиты
│   ├── __init__.py           # Пакет utils
│   ├── api_client.py         # Клиент для API-запросов
│   └── analyze_page.py       # Утилиты анализа страниц
│
├── 📄 .gitignore             # Исключаемые файлы Git
├── 📄 pytest.ini             # Конфигурация pytest
├── 📄 README.md              # Описание проекта
└── 📄 requirements.txt       # Зависимости Python
## Запуск тестов
Запуск ВСЕХ тестов (UI + API)
# Простой запуск
pytest

# С подробным выводом
pytest -v

# С созданием отчёта Allure
pytest --alluredir=allure-results
allure serve allure-results

Запуск ТОЛЬКО UI-тестов
# По имени файла
pytest tests/test_ui.py

# По маркеру (если тесты помечены маркерами)
pytest -m ui

# С указанием пути
pytest tests/ -k "ui" -v

# С генерацией HTML-отчёта
pytest tests/test_ui.py --html=report_ui.html

Запуск ТОЛЬКО API-тестов
# По имени файла
pytest tests/test_api.py

# По маркеру
pytest -m api

# Только API-тесты с детальным логом
pytest tests/test_api.py -v

# С сохранением результатов в JSON
pytest tests/test_api.py --json=api_results.json