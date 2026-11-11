python 3.14.3 версии

Приложение предоставляет GET /health и возвращает {"status": "OK"}.
Базу этот маршрут не проверяет.

Перед установкой зависимостей нужно создать и активировать виртуальное окружение Python.
Запуск установки зависимостей: python -m pip install -r requirements.txt

Файл .env: создать сам файл в корне и скопировать содержимое из .env.example.
Указать нужные логин, пароль и название базы данных

Для запуска PostgreSQL необходим работающий Docker Desktop.
База пока не подключена к приложению FastAPI.
Запуска PostgreSQL: docker compose up -d postgres

Запуск FastAPI: python -m uvicorn main:app --reload
Запуск /health: curl http://localhost:8000/health
Запуск тестов: python -m pytest -v
