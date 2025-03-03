import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Подключаем конфигурацию Alembic
config = context.config

# Настраиваем логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Импортируем модели для автогенерации миграций
from app.models import Base  # Замени 'app.models' на путь к твоим моделям

# Указываем метаданные моделей
target_metadata = Base.metadata

# Загружаем URL базы данных из alembic.ini или переопределяем
config.set_main_option(
    "sqlalchemy.url", os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:Abuka2004@localhost/ayauSQL")
)


def run_migrations_offline() -> None:
    """Запускаем миграции в offline-режиме."""
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
    """Запускаем миграции в online-режиме."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
