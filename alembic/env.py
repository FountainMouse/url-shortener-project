import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# -----------------------------------------------------
# BOB'S FIX: Import necessary components from the application
# Add the project root to the sys path to allow imports from 'app'
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# Import application components
from app.settings import settings
from app.models.base import Base 
# -----------------------------------------------------

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python's standard logging.
# This ensures that Alembic logging is set up correctly.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target metadata object for 'autogenerate' support
# This tells Alembic which SQLAlchemy models to track.
target_metadata = Base.metadata

# other values from the config, defined by the user can be
# accessed: target_database_server, etc.
# my_important_option = config.get_main_option("my_important_option")
# ...

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By not using an Engine, we don't actually
    connect to the database.

    """
    # BOB'S FIX: Use the URL from application settings
    url = settings.database_url
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario, we need to create an Engine
    and associate a connection with the context.

    """
    # BOB'S FIX: Prepare the configuration for the engine
    configuration = config.get_section(config.config_ini_section)
    
    # BOB'S FIX: Override the sqlalchemy.url option with the one from app settings
    configuration['sqlalchemy.url'] = settings.database_url
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
