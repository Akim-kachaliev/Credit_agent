import sys
from pathlib import Path

# Добавляем корневую папку проекта в путь поиска модулей
# Это нужно чтобы импорты работали правильно
sys.path.append(str(Path(__file__).parent.parent))

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Импортируем наши модели
from app.database import Base
from app import models  # Это чтобы Alembic увидел все модели

# Это объект конфигурации Alembic
# Он предоставляет доступ к значениям в файле alembic.ini
config = context.config

# Настраиваем логгирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем Alembic, откуда брать метаданные моделей
# Base.metadata содержит информацию о всех таблицах
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """
    Запуск миграций в 'оффлайн' режиме.
    Используется когда нет подключения к базе данных.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """
    Запуск миграций в 'онлайн' режиме.
    Используется когда есть подключение к базе данных.
    """
    # Получаем настройки подключения из конфига
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Подключаемся к базе и выполняем миграции
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,      # Сравнивать типы колонок
            compare_server_default=True,  # Сравнивать значения по умолчанию
        )

        with context.begin_transaction():
            context.run_migrations()

# Определяем, в каком режиме запускать миграции
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()