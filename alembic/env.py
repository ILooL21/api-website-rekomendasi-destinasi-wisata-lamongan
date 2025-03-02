from logging.config import fileConfig
from sqlalchemy import pool, engine_from_config
from alembic import context
from app.core.config import settings

# Konfigurasi Alembic
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata model untuk autogenerate
from app.db.models import Base # Import Base yang mengandung metadata
import app.db.models

target_metadata = Base.metadata  # Gunakan metadata dari model SQLAlchemy

# Menggunakan database URL dari settings.py
config.set_main_option("sqlalchemy.url", settings.database_url)


def run_migrations_offline() -> None:
    """Jalankan migrasi dalam mode offline (tanpa koneksi langsung ke database)."""
    context.configure(
        url=settings.database_url,  # Ambil dari settings
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,  # Gunakan Base.metadata untuk mendeteksi model
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
