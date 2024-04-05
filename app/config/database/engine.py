from sqlalchemy import create_engine

from ..settings import get_settings

__all__ = ["engine"]

SQLALCHEMY_DATABASE_URL = (
    "postgresql://"
    + get_settings().DB_USER
    + ":"
    + get_settings().DB_PASS
    + "@"
    + get_settings().DB_HOST
    + ":"
    + get_settings().DB_PORT
    + "/"
    + get_settings().DB_NAME
)

if get_settings().ENVIRONMENT == "development":
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
