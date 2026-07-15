# Credit agent

Приложение дял автоматической проверки пакетов документов по кредитным программам.

---

## О проекте 

Этот проект я делал в рамках тестового задания для позиции Backend-разработчика для проекта. Суть проекта: сотрудники, вручную проверяют документы по кредитам, а нам надо автоматизировать этот процесс. Загружаешь файлы — система сама проверяет, всё ли на месте, и выдаёт результат.

**Что умеет:**
- Принимает файлы (договор, спецификация, счёт, акт)
- Проверяет, все ли документы загружены
- Смотрит, правильные ли форматы (PDF, DOCX, JPG, PNG)
- Проверяет размер файлов (не больше 20 МБ)
- Определяет тип документа по названию файла
- Сохраняет историю проверок в базу данных
- Возвращает статус: всё ок, есть ошибки или только предупреждения

---

## Технологии использования

| Технология |
|------------|
| **Python 3.11** | | **FastAPI** | | **PostgreSQL** | | **SQLAlchemy** | | **Alembic** | | **Pydantic** | | **Docker** | | **Pytest** |

---

**Структура проекта**
Credit_agent/
│
├── app/                              # Основной код
│   ├── routers/                      # API
│   │   ├── checks.py                # Эндпоинты
│   │   └── __init__.py
│   ├── services/                     # Логика
│   │   ├── check_service.py          # Обработка проверки
│   │   ├── validation_service.py     # Проверка документов
│   │   └── __init__.py
│   ├── utils/                        # Вспомогательное
│   │   ├── file_utils.py            # Работа с файлами
│   │   └── __init__.py
│   ├── __init__.py
│   ├── database.py                   # Подключение к БД
│   ├── main.py                       # Точка входа
│   ├── models.py                     # Модели БД
│   └── schemas.py                    # Схемы API
│
├── tests/                            # Тесты
│   ├── __init__.py
│   ├── test_api.py
│   └── test_validation.py
│
├── migrations/                       # Миграции
│   ├── versions/
│   ├── __init__.py
│   ├── env.py
│   └── script.py.mako
│
├── test_files/                       # Тестовые файлы
│   ├── акт.pdf
│   ├── договор.pdf
│   ├── спецификация.pdf
│   └── счёт.pdf
│
├── .env.example                      # Пример настроек
├── .gitignore                        # Игнорируемые файлы
├── alembic.ini                       # Конфиг миграций
├── docker-compose.yml                # Docker Compose
├── Dockerfile                        # Docker
├── requirements.txt                  # Зависимости
└── README.md                         # Документация

## Как запустить проект

### Вариант 1: Через Docker (самый простой)

**Что нужно:**
- Установленный Docker Desktop
- Установленный Git

**Шаг 1. Клонируем репозиторий**
Откройте командную строку и выполните:
git clone https://github.com/Akim-kachaliev/Credit_agent.git
cd Credit_agent

**Шаг 2. Создаём файл с настройками**
cp .env.example .env

**Шаг 3. Запускаем проект**
docker-compose up --build

**Шаг 4. Проверяем, что работает**
Откройте браузер и перейдите по адресам:

Что проверяем	            Адрес
Документация API	http://localhost:8000/docs
Проверка здоровья	http://localhost:8000/health
ReDoc	http://localhost:8000/redoc

**Как запустить тесты через Docker**
docker-compose exec app pytest tests/ -v

**Как создать тестовые файлы для проверки**
# Создаём папку
mkdir test_files

# Командная строка (cmd)
echo Тестовый договор > test_files\договор.pdf
echo Тестовая спецификация > test_files\спецификация.pdf
echo Тестовый счёт > test_files\счёт.pdf
echo Тестовый акт > test_files\акт.pdf

**Как проверить API через Swagger**
Шаг 1. Откройте браузер и перейдите по адресу:
http://localhost:8000/docs

Шаг 2. Найдите эндпоинт POST /api/checks
Шаг 3. Нажмите "Try it out"
Шаг 4. Заполните поля:
program: выберите federal или regional
files: нажмите "Choose Files" и выберите файлы из папки test_files
Шаг 5. Нажмите "Execute"
Шаг 6. Посмотрите результат:
Если загрузили все 4 файла → статус approved
Если загрузили только 1 файл → статус rejected
Если загрузили файл с неизвестным именем → статус check_in_progress

**Как проверить API через командную строку**
curl -X POST "http://localhost:8000/api/checks/" -F "program=federal" -F "files=@test_files\договор.pdf" -F "files=@test_files\спецификация.pdf" -F "files=@test_files\счёт.pdf" -F "files=@test_files\акт.pdf"

**Как посмотреть список проверок через командную строку**
http://localhost:8000/api/checks/

**Как работать с миграциями базы данных**

**Создать миграцию**
docker-compose exec app alembic revision --autogenerate -m "Описание изменений"

**Накатить миграции**
docker-compose exec app alembic upgrade head

**Откатить миграцию**
docker-compose exec app alembic downgrade -1

**Проверить текущую версию**
docker-compose exec app alembic current

**Посмотреть историю миграций**
docker-compose exec app alembic history

**Как остановить проект через Docker**
В терминале, где запущен сайт, нажмите Ctrl + C, затем:
docker-compose down

**Как пересобрать проект**
Останавливаем
docker-compose down

Удаляем старые образы (опционально)
docker-compose down -v

Пересобираем и запускаем
docker-compose up --build

**Как проверить, что база данных работает через терминал**
Заходим в контейнер с БД
docker-compose exec db psql -U user -d credit_db

Смотрим таблицы
\dt

Смотрим данные в таблице checks
SELECT * FROM checks;

Выходим
\q

**Проверить через код**
curl http://localhost:8000/health
Должен вернуть: {"status":"healthy"}
