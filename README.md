# Credit Document Checker API

API сервис для автоматической проверки пакетов документов по кредитным программам.

## Технологии

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- Pytest

## Быстрый старт

```bash
# Клонируем репозиторий
git clone <repository-url>
cd credit-document-checker

# Копируем .env
cp .env.example .env

# Запускаем через Docker
docker-compose up --build