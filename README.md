<p align="center">
  <h1 align="center">Credit Agent</h1>
  <p align="center">
    <strong>Автоматическая проверка пакетов документов по кредитным программам</strong>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.11">
  <img src="https://img.shields.io/badge/FastAPI-0.104.1-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0.23-D71F00?style=flat-square&logo=python&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Pytest-7.4.3-0A9EDC?style=flat-square&logo=pytest&logoColor=white" alt="Pytest">
</p>

---

## О проекте

Тестовое задание на позицию **Backend-разработчик**. Проект автоматизирует рутинный процесс ручной проверки кредитных документов: пользователь загружает файлы, система валидирует пакет и мгновенно возвращает результат.

### Возможности

| Возможность | Описание |
|:------------|:---------|
| :page_facing_up: Приём файлов | Договор, спецификация, счёт, акт |
| :clipboard: Комплектность | Проверка наличия всех обязательных документов |
| :file_folder: Валидация форматов | PDF, DOCX, JPG, PNG |
| :weight_lifting: Ограничение размера | Максимальный размер файла — 20 МБ |
| :mag: Распознавание типов | Определение типа документа по ключевым словам в имени файла |
| :database: История проверок | Все результаты сохраняются в PostgreSQL |
| :white_check_mark: Понятный статус | `approved`, `rejected` или `check_in_progress` с деталями |

---

## Технологический стек

| Технология | Версия | Назначение |
|:-----------|:-------|:-----------|
| Python | 3.11 | Язык разработки |
| FastAPI | 0.104.1 | Веб-фреймворк |
| PostgreSQL | 15 | База данных |
| SQLAlchemy | 2.0.23 | ORM |
| Alembic | 1.12.1 | Миграции БД |
| Pydantic | 2.5.0 | Валидация данных |
| Docker Compose | — | Контейнеризация |
| Pytest | 7.4.3 | Тестирование |

---

## Структура проекта

```
Credit_agent/
├── app/                          # Основной код приложения
│   ├── routers/
│   │   ├── checks.py             # API-эндпоинты проверок
│   │   └── __init__.py
│   ├── services/
│   │   ├── check_service.py      # Оркестрация процесса проверки
│   │   ├── validation_service.py # Непосредственная валидация
│   │   └── __init__.py
│   ├── utils/
│   │   ├── file_utils.py         # Работа с файлами
│   │   └── __init__.py
│   ├── __init__.py
│   ├── database.py               # Подключение к БД
│   ├── main.py                   # Точка входа
│   ├── models.py                 # Модели SQLAlchemy
│   └── schemas.py                # Схемы Pydantic
│
├── tests/                        # Автотесты
│   ├── __init__.py
│   ├── test_api.py               # Тесты API
│   └── test_validation.py        # Тесты логики валидации
│
├── migrations/                   # Миграции (Alembic)
│   ├── versions/
│   ├── __init__.py
│   ├── env.py
│   └── script.py.mako
│
├── test_files/                   # Тестовые файлы
│   ├── договор.pdf
│   ├── спецификация.pdf
│   ├── счёт.pdf
│   └── акт.pdf
│
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Быстрый старт

### Что должно быть установлено

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

### 1. Клонирование

```bash
git clone https://github.com/Akim-kachaliev/Credit_agent.git
cd Credit_agent
```

### 2. Настройка окружения

```bash
cp .env.example .env
```

### 3. Сборка и запуск

```bash
docker-compose up --build
```

### 4. Проверка

| Что проверяем | Адрес |
|:--------------|:------|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Healthcheck | http://localhost:8000/health |

---

## API

### `POST /api/checks/` — Проверка пакета документов

**Параметры запроса** (`multipart/form-data`):

| Поле | Тип | Обязательный | Описание |
|:-----|:----|:-------------|:---------|
| `program` | string | Да | Кредитная программа: `federal` или `regional` |
| `files` | file[] | Да | Загружаемые документы (1–4 файла) |

**Пример запроса** (`curl`):

```bash
curl -X POST "http://localhost:8000/api/checks/" \
  -F "program=federal" \
  -F "files=@test_files/договор.pdf" \
  -F "files=@test_files/спецификация.pdf" \
  -F "files=@test_files/счёт.pdf" \
  -F "files=@test_files/акт.pdf"
```

**Пример ответа** (`200 OK`):

```json
{
  "id": 1,
  "program": "federal",
  "status": "approved",
  "details": {
    "total_files": 4,
    "recognized": ["contract", "specification", "invoice", "act"],
    "errors": [],
    "warnings": []
  },
  "created_at": "2025-01-15T12:00:00"
}
```

**Возможные статусы:**

| Статус | Условие | Описание |
|:-------|:--------|:---------|
| `approved` | Все 4 документа загружены | Пакет прошёл проверку |
| `rejected` | Пропущен хотя бы один обязательный документ | Пакет неполный |
| `check_in_progress` | Загружен файл с неопределённым типом | Требуется ручная проверка |

### `GET /api/checks/` — История проверок

Возвращает список всех проведённых проверок с пагинацией.

---

## Тестирование

### Запуск тестов

```bash
docker-compose exec app pytest tests/ -v
```

### Создание тестовых файлов

**Linux / macOS:**

```bash
mkdir -p test_files
echo "Тестовый договор"       > test_files/договор.pdf
echo "Тестовая спецификация"  > test_files/спецификация.pdf
echo "Тестовый счёт"          > test_files/счёт.pdf
echo "Тестовый акт"           > test_files/акт.pdf
```

**Windows (cmd):**

```cmd
mkdir test_files
echo Тестовый договор > test_files\договор.pdf
echo Тестовая спецификация > test_files\спецификация.pdf
echo Тестовый счёт > test_files\счёт.pdf
echo Тестовый акт > test_files\акт.pdf
```

---

## Миграции (Alembic)

| Действие | Команда |
|:---------|:--------|
| Создать миграцию | `docker-compose exec app alembic revision --autogenerate -m "Описание"` |
| Применить миграции | `docker-compose exec app alembic upgrade head` |
| Откатить миграцию | `docker-compose exec app alembic downgrade -1` |
| Текущая версия | `docker-compose exec app alembic current` |
| История миграций | `docker-compose exec app alembic history` |

---

## Переменные окружения

Файл `.env` создаётся из `.env.example`:

```env
DATABASE_URL=postgresql://user:password@db:5432/credit_db
SECRET_KEY=your-secret-key-here
```

| Переменная | Описание |
|:-----------|:---------|
| `DATABASE_URL` | Строка подключения к PostgreSQL |
| `SECRET_KEY` | Секретный ключ приложения |

---

## Управление Docker

| Действие | Команда |
|:---------|:--------|
| Запуск | `docker-compose up --build` |
| Остановка | `docker-compose down` |
| Очистка с удалением данных БД | `docker-compose down -v` |

---

## Проверка состояния БД

```bash
# Подключение к PostgreSQL
docker-compose exec db psql -U user -d credit_db
```

```sql
-- Список таблиц
\dt

-- Все записи проверок
SELECT * FROM checks;

-- Выход
\q
```

---
