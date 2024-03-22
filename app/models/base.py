import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True
    # since there is no schema it will place it in the public schema
    # this is the default schema for all tables that dont have a schema
    # this will new happen cause whnever we get the database we will select the correct schema
    # default schema is the public schema but now we are using the tenant schema as the default schema so if any table is missing a schema we will notice it
    metadata = sa.MetaData(schema="tenant")  # random schema to avoid placing the tables in the public schema

    #    note tenant only exists on local machine and not on the server on the server the default schema is the the tenant_default schema this is to avoid placing the tables in the public schema
    # and we need it for the create all models to work correctly and we dont need that on the server so we will remove it from the server
