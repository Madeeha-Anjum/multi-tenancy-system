import logging
import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import MetaData, engine_from_config, pool, text

from src.multi_tenancy_system.models.base import Base

load_dotenv()  # Load environment variables from .env file

# Alembic Config object used to run alembic commands
config = context.config

# Configure logging based on Alembic config file
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Example usage of the logger
logging.info("\n\033[93mStarting Alembic script\033[0m\n")

# Get database connection parameters from environment variables
db_user, db_pass, db_host, db_port, db_name = (
    os.getenv("DB_USER"),
    os.getenv("DB_PASS"),
    os.getenv("DB_HOST"),
    os.getenv("DB_PORT"),
    os.getenv("DB_NAME"),
)

# Validate required environment variables
if None in (db_user, db_pass, db_host, db_port, db_name):
    raise ValueError("\n\033[91mOne or more required environment variables are not set\033[0m\n")

# Set SQLAlchemy URL in Alembic config
config.set_main_option(
    "sqlalchemy.url",
    f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}",
)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DB API to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=f"postgresql://{db_user}:xxxxxxxxx@xxxxxxxxx:{db_port}/{db_name}",
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    naming_convention = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    translated = MetaData(naming_convention=naming_convention)

    def translate_schema(table, to_schema, constraint, referred_schema):
        return to_schema

    for table in Base.metadata.tables.values():
        schema = "tenant_default" if not table.schema else table.schema
        table.schema = translate_schema(table, schema, None, None)

        print(f"\n\033[95m Running on schema {schema}\033[0m\n")

    # Create engine from Alembic config
    connectable = engine_from_config(
        config.get_section(
            config.config_ini_section, {}
        ),  # get the section from the config file that specifies the database connection
        prefix="sqlalchemy.",  # prefix to strip from the url
        poolclass=pool.NullPool,  # no reuse of connections
    )

    # Connect to database
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=translated,
            compare_type=True,
            transaction_per_migration=True,
            include_schemas=True,
        )
        with context.begin_transaction():
            try:
                context.run_migrations()
                logging.info("\n\033[92mAlembic script finished\033[0m\n")
            except Exception as e:
                logging.error(f"\033[91mError running migrations: {e}\033[0m")
                context.get_context().connection.execute(text("ROLLBACK"))


if context.is_offline_mode():
    """
    Run migrations in 'offline' mode using --sql option.
    """
    run_migrations_offline()
else:
    """Run migrations in 'online' mode. (default mode)"""
    run_migrations_online()
