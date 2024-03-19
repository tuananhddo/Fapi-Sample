from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv
import os
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
current_file_path = os.path.abspath(__file__)
# Get the directory containing the current Python script file
current_directory = os.path.dirname(current_file_path)
print("Current directory:", current_directory)

from src.models.base import Base
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
# Load DB
# engine = os.environ.get("DB_ENGINE")
# dbhost = os.environ.get("DB_HOST")
# username = os.environ.get("DB_USERNAME")
# password = os.environ.get("DB_PASSWORD")
# dbname = os.environ.get("DB_NAME")

# config.set_main_option("sqlalchemy.url", f"{engine}://{username}:{password}@{dbhost}/{dbname}")
def get_url():
    local_run = os.getenv("RUN_LOCAL", True)
    if local_run:
        load_dotenv()
    engine = os.getenv("DB_ENGINE", "postgresql+psycopg2")
    user = os.getenv("DB_USERNAME", "postgres")
    password = os.getenv("DB_PASSWORD", "1")
    server = os.getenv("DB_HOST", "db")
    port = os.getenv("DB_PORT", "5432")
    db = os.getenv("DB_NAME", "app")
    return f"{engine}://{user}:{password}@{server}:{port}/{db}"

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url")
    url = get_url()
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

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
