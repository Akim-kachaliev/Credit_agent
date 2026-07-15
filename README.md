# Credit Agent

Приложение для автоматической проверки пакетов документов по кредитным программам.

---

## О проекте 

Этот проект разработан в рамках тестового задания на позицию Backend-разработчика.

**Суть проекта:** Автоматизация рутинного процесса ручной проверки кредитных документов сотрудниками. Пользователь загружает файлы — система автоматически валидирует пакет документов и мгновенно выдает результат.

---

### Что умеет система:

- **Принимает файлы:** Договор, спецификация, счёт, акт.
- **Контролирует комплектность:** Проверяет, все ли обязательные документы загружены.
- **Валидирует форматы:** Поддерживает форматы PDF, DOCX, JPG, PNG.
- **Ограничивает размер:** Файлы не должны превышать 20 МБ.
- **Распознает типы:** Определяет тип документа по ключевым словам в названии файла.
- **Ведет историю:** Сохраняет результаты и историю всех проверок в базу данных PostgreSQL.
- **Выводит понятный статус:** Возвращает вердикт (approved, rejected или check_in_progress) с детальным описанием ошибок или предупреждений.

---

## Технологический стек

| Технология | Версия |
|------------|--------|
| **Язык разработки** | Python 3.11 |
| **Фреймворк** | FastAPI 0.104.1 |
| **База данных** | PostgreSQL 15 |
| **ORM** | SQLAlchemy 2.0.23 |
| **Миграции** | Alembic 1.12.1 |
| **Валидация данных** | Pydantic 2.5.0 |
| **Контейнеризация** | Docker / Docker Compose |
| **Тестирование** | Pytest 7.4.3 |

text

---

## Структура проекта
Credit_agent/
│
├── app/ # Основной код приложения
│ ├── routers/ # API Эндпоинты
│ │ ├── checks.py # Роуты для проверок
│ │ └── init.py
│ ├── services/ # Бизнес-логика
│ │ ├── check_service.py # Оркестрация процесса проверки
│ │ ├── validation_service.py # Непосредственная валидация
│ │ └── init.py
│ ├── utils/ # Вспомогательные утилиты
│ │ ├── file_utils.py # Работа с файлами
│ │ └── init.py
│ ├── init.py
│ ├── database.py # Настройка подключения к БД
│ ├── main.py # Точка входа в приложение
│ ├── models.py # Описание таблиц SQLAlchemy
│ └── schemas.py # Схемы валидации Pydantic
│
├── tests/ # Автотесты
│ ├── init.py
│ ├── test_api.py # Тестирование API эндпоинтов
│ └── test_validation.py # Тестирование логики валидации
│
├── migrations/ # Миграции базы данных (Alembic)
│ ├── versions/ # Файлы миграций
│ ├── init.py
│ ├── env.py # Конфигурация Alembic
│ └── script.py.mako # Шаблон для создания миграций
│
├── test_files/ # Тестовые файлы для ручной проверки
│ ├── акт.pdf
│ ├── договор.pdf
│ ├── спецификация.pdf
│ └── счёт.pdf
│
├── .env.example # Пример конфигурационного файла
├── .gitignore # Исключения для Git
├── alembic.ini # Конфигурация Alembic
├── docker-compose.yml # Сценарий Docker Compose
├── Dockerfile # Инструкции сборки контейнера
├── requirements.txt # Зависимости проекта
└── README.md # Документация проекта

text

---

## Как запустить проект

### Запуск через Docker

**Пререквизиты:** На вашем компьютере должны быть установлены Docker Desktop и Git.

**Шаг 1. Клонирование репозитория**

```bash
git clone https://github.com/Akim-kachaliev/Credit_agent.git
cd Credit_agent

---

**Шаг 2. Настройка окружения**

bash
cp .env.example .env


**Шаг 3. Сборка и запуск контейнеров**

bash
docker-compose up --build


**Шаг 4. Проверка работоспособности**

Что проверяем	Адрес в браузере
Интерактивная документация (Swagger)	http://localhost:8000/docs
Альтернативная документация (ReDoc)	http://localhost:8000/redoc
Проверка статуса (Healthcheck)	http://localhost:8000/health

**Инструкции по работе с проектом**
1. Тестирование
Запуск тестов:

bash
docker-compose exec app pytest tests/ -v
Создание тестовых файлов:

bash
mkdir test_files
Для Windows (cmd):

cmd
echo Тестовый договор > test_files\договор.pdf
echo Тестовая спецификация > test_files\спецификация.pdf
echo Тестовый счёт > test_files\счёт.pdf
echo Тестовый акт > test_files\акт.pdf
Для Linux / macOS (bash):

bash
echo "Тестовый договор" > test_files/договор.pdf
echo "Тестовая спецификация" > test_files/спецификация.pdf
echo "Тестовый счёт" > test_files/счёт.pdf
echo "Тестовый акт" > test_files/акт.pdf

2. Взаимодействие с API
Через Swagger (рекомендуется):

Перейдите на http://localhost:8000/docs

Раскройте эндпоинт POST /api/checks

Нажмите "Try it out"

Укажите параметры:

program: выберите federal или regional

files: выберите файлы из папки test_files

Нажмите "Execute"

Поведение системы:

Сценарий	Результат
Загружены все 4 обязательных файла	✅ статус approved
Пропущен хотя бы один файл	❌ статус rejected
Загружен файл с неопределенным типом	⚠️ статус check_in_progress
Проверка через консоль (curl):

bash
curl -X POST "http://localhost:8000/api/checks/" \
  -F "program=federal" \
  -F "files=@test_files/договор.pdf" \
  -F "files=@test_files/спецификация.pdf" \
  -F "files=@test_files/счёт.pdf" \
  -F "files=@test_files/акт.pdf"
Просмотр истории проверок:

text
http://localhost:8000/api/checks/

3. Работа с миграциями базы данных (Alembic)
Действие	Команда
Создать миграцию	docker-compose exec app alembic revision --autogenerate -m "Описание"
Применить миграции	docker-compose exec app alembic upgrade head
Откатить миграцию	docker-compose exec app alembic downgrade -1
Проверить версию	docker-compose exec app alembic current
История миграций	docker-compose exec app alembic history


4. Управление Docker-окружением
Остановка контейнеров:

bash
docker-compose down
Полная очистка (с удалением данных БД):

bash
docker-compose down -v
Пересборка и чистый запуск:

bash
docker-compose up --build
5. Проверка состояния БД
bash
# Входим в контейнер PostgreSQL
docker-compose exec db psql -U user -d credit_db

# Смотрим список таблиц (внутри psql)
\dt

# Выбрать все записи проверок
SELECT * FROM checks;

# Выйти из psql
\q
Переменные окружения
Создайте файл .env в корне проекта:

env
DATABASE_URL=postgresql://user:password@db:5432/credit_db
SECRET_KEY=your-secret-key-here
Переменная	Описание
DATABASE_URL	Строка подключения к базе данных
SECRET_KEY	Секретный ключ для приложения
