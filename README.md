Lite Message: Учебный backend мессенджера на Python.

Проект разрабатывается постепенно для практики создания REST API, работы с PostgreSQL, SQLAlchemy, миграциями, транзакциями, авторизацией и Git.

Стек:
- Python 3.14
- FastAPI
- Pydantic v2
- SQLAlchemy 2
- PostgreSQL 16
- Alembic
- PyJWT
- Argon2
- Pytest
- Docker Compose
- GitHub Actions

Реализовано
- Проверка работоспособности приложения через GET /health
- Регистрация пользователей
- Валидация и нормализация email и username
- Проверка уникальности email и username
- Хеширование паролей через Argon2
- Вход по email и паролю
- JWT-аутентификация
- Проверка подписи и срока действия JWT
- Отзыв токенов через token_version
- Получение профиля текущего пользователя
- Частичное изменение username и display name
- Поиск пользователей по началу username
- Пагинация поиска через limit и offset
- Отправка заявок в контакты
- Получение входящих заявок
- Принятие заявок
- Отклонение заявок
- Удаление принятого контакта
- Получение списка принятых контактов
- Защита от встречных дубликатов контактов на уровне PostgreSQL
- Отправка сообщений принятым контактам
- Отправка сообщений самому себе
- Получение истории диалога
- Курсорная пагинация истории через before_id
- Ограничение размера сообщений
- Проверка доступа к контактам и диалогам
- Миграции базы данных через Alembic
- Локальный запуск PostgreSQL через Docker Compose
- Автоматический запуск миграций и тестов через GitHub Actions

Архитектура:
Проект разделен на несколько слоев.

HTTP-маршрут -> Сервис -> Репозиторий -> PostgreSQL

Маршруты принимают HTTP-запросы и формируют ответы.
Pydantic-схемы проверяют входные данные и описывают структуру ответов.
Сервисы содержат бизнес-правила и управляют транзакциями.
Репозитории выполняют запросы к базе данных. Репозитории не делают скрытый commit.

Основные маршруты
    Служебный маршрут:
    GET /health - Возвращает статус приложения.
    
    Пользователи:
    POST /users
    POST /users/login
    GET /users/me
    PATCH /users/me
    GET /users/search
    
    Контакты: 
    POST /contacts/{addressee_id}
    GET /contacts/incoming
    PATCH /contacts/accept/{requester_id}
    DELETE /contacts/decline/{requester_id}
    DELETE /contacts/delete/{peer_id}
    GET /contacts/accepted
    
    Сообщения
    POST /messages/{recipient_id}
    GET /messages/dialog_with/{other_user}
    
    История сообщений поддерживает загрузку частями.




    Пример получения последних сообщений:
    GET /messages/dialog_with/6?limit=30

    Пример получения более старых сообщений:
    GET /messages/dialog_with/6?limit=30&before_id=25

Для защищенных маршрутов используется заголовок:
Authorization: Bearer YOUR_ACCESS_TOKEN

Запуск проекта:
    Для запуска PostgreSQL нужен Docker Desktop.

    Создайте виртуальное окружение:
    python -m venv .venv

    Активируйте виртуальное окружение в Git Bash:
    source .venv/Scripts/activate

    Установите зависимости:
    python -m pip install -r requirements.txt

    Создайте в корне проекта файл .env. Скопируйте в него настройки из .env.example и укажите свои локальные значения.

    Пример настроек:
    POSTGRES_USER=user
    POSTGRES_PASSWORD=your_local_password
    POSTGRES_DB=lite_message
    POSTGRES_HOST=127.0.0.1
    POSTGRES_PORT=5433
    JWT_SECRET_KEY=your_local_secret_key
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    ! Файл .env не должен добавляться в Git. В нем находятся локальный пароль базы данных и секретный ключ JWT.

Запустите PostgreSQL:
docker compose up -d postgres

Проверьте состояние контейнера:
docker compose ps

Примените миграции:
python -m alembic upgrade head

Запустите FastAPI:
python -m uvicorn main:app --reload

Приложение будет доступно по адресу:
http://127.0.0.1:8000

Проверьте health endpoint:
curl -i http://127.0.0.1:8000/health

Запустите все тесты:
python -m pytest -v

Тесты проверяют health endpoint, Pydantic-схемы, хеширование паролей и регистрацию пользователя через отдельную PostgreSQL-базу.

GitHub Actions автоматически устанавливает зависимости, запускает PostgreSQL, применяет миграции и запускает тесты.

Миграции
    Создание новой миграции:
    python -m alembic revision --autogenerate -m "Migration description"

    Перед применением автоматически созданную миграцию нужно проверить вручную.

    Применение миграций:
    python -m alembic upgrade head

    Откат на одну миграцию:
    python -m alembic downgrade -1

    Для работы с тестовой базой используется отдельное имя базы и отдельный запуск миграций.

Git
Функциональность разрабатывается в отдельных feature-ветках.

Создание ветки:
git switch -c feature/example

Проверка изменений:
git status
git diff

После завершения задачи изменения отправляются на GitHub и добавляются в Pull Request.

Основная ветка проекта: main

Статус проекта: находится в разработке.

Следующие задачи:
- Редактирование сообщений
- Мягкое удаление сообщений
- Блокировки пользователей
- Непрочитанные сообщения
- Список диалогов
- Ограничение запросов через Redis
- Расширение автоматических тестов
- Развертывание на сервере


Автор: Anid94

Прокект на GitHub:
https://github.com/Anid94/lite_message