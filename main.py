from contextlib import contextmanager
from enum import Enum
from typing import Optional

import alembic
import sqlalchemy as sa
from alembic.config import Config
from alembic.migration import MigrationContext
from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import get_settings
from app.models.base import Base

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

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
# -----------------------------------------------------


class Status(Enum):
    active = "active"
    inactive = "inactive"


class Tenant(Base):
    # NOTE: we want tp place the tenants in the shared schema becase we dont want to use public becase
    # ALL tables that dont have a schema will be placed in the public schema, this way if any tables are missing a scema we will notice it
    __tablename__ = "tenants"
    # add help text to the columns
    id = sa.Column(
        "id",
        sa.Integer,
        primary_key=True,
        nullable=False,
        comment="The unique identifier for the tenant",
    )
    name = sa.Column(
        "name",
        sa.String(256),
        nullable=False,
        index=True,
        unique=True,
        comment="the name of the tenant example: site1",
    )
    schema = sa.Column(
        "schema",
        sa.String(256),
        nullable=False,
        unique=True,
        comment="The schema for the database of the tenant example: site1",
    )
    host = sa.Column(
        "host",
        sa.String(256),
        nullable=False,
        unique=True,
        comment="The host of the tenant example: site1.localhost",
    )
    status = sa.Column(
        "status",
        sa.Enum(Status, inherit_schema=True),
        nullable=False,
        comment="The status of the tenant",
    )  # inherit_schema=True will place the enum in the correct schema and not in the public schema

    __table_args__ = ({"schema": "shared"},)


class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, index=True)
    email = sa.Column(sa.String, unique=True, index=True)
    degree = sa.Column(sa.String, index=True)


# -----------------------------------------------------


def get_shared_metadata():
    """Get the metadata for the shared schema"""
    meta = MetaData()
    for table in Base.metadata.tables.values():
        if table.schema != "tenant":
            table.tometadata(meta)
    return meta


def get_tenant_specific_metadata():
    meta = MetaData(schema="tenant")
    for table in Base.metadata.tables.values():
        if table.schema == "tenant":
            table.tometadata(meta)
    return meta


# this is us purposefully selecting the schema we want to use instead of using the port and host names to select the schema
@contextmanager
def with_db(tenant_schema: Optional[str]):
    """Get a database connection for the given tenant schema"""
    if tenant_schema:
        schema_translate_map = dict(tenant=tenant_schema)
    else:
        schema_translate_map = None

    connectable = engine.execution_options(schema_translate_map=schema_translate_map)

    try:
        db = Session(autocommit=False, autoflush=False, bind=connectable)
        yield db
    finally:
        db.close()


# Run create_all() only in development or test environment
# if os.getenv('ENVIRONMENT', 'development') in ('development', 'test'):
# create tenant schema if not exists
#  we dont need to create_all() we can just run migrations on the new schema
# Base.metadata.create_all(bind=engine, checkfirst=True)

# Base.metadata.create_all(bind=engine)

# dont use this anymore
# Create a tenant defult schema in alembic
# alembic revision --autogenerate -m "create tenant_default schema"
# then add the following to the upgrade function
# op.execute('CREATE SCHEMA tenant_default')
# then run the migration
# alembic upgrade head
# then add the following to the downgrade function but we dont need to run the downgrade function ever so we can just remove it its safer that way
# op.execute('DROP SCHEMA tenant_default')
# then ENV="development" in alembic tno repload with some data and then run the migration
# alembic upgrade head then it will create all tables for all tenants

# first finish the alembic stuff

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -----------------------------------------------------

# async def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# automattically get the tenant from the request header based on host and port and return corredct db session
def get_tenant(req: Request) -> Tenant:
    """Get the tenant based on the request header"""
    host_without_port = req.headers["host"].split(":", 1)[0]
    print(f"\n, host_without_port={host_without_port}\n")
    with with_db(None) as db:
        tenant = db.query(Tenant).filter(Tenant.host == host_without_port).one_or_none()

    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return tenant


def get_db(tenant: Tenant = Depends(get_tenant)):
    """Get the database session for the current tenant"""
    with with_db(tenant.schema) as db:
        yield db  # returning the db and then completed when the function is done


# -----------------------------------------------------

app = FastAPI()


@app.get("/info")
async def info():
    return {
        "app_name": get_settings().app_name,
    }


@app.get("/")
def read_root(request: Request):
    return {"Host": request.headers["host"]}


class UserBase(BaseModel):
    name: str
    email: str
    degree: Optional[str]


@app.get("/users", response_model=UserBase)
def read_user(db: Session = Depends(get_db)):
    # use database
    # stmt = (
    #     select(Tenant)
    # )

    # result = db.execute(stmt).all()
    # # https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#new-result-object
    # for user in result.scalars():
    #     print(user.to_dict())
    #     user._asdict()
    #     user._fields()
    #     user._mapping()
    #     user._t()
    #     user._tuple()

    #     import sys; print(f'\n{sys._getframe().f_lineno}-{__name__}=====> \033[93muser { user }\033[0m\n')

    # tenants = db.query(Tenant).all()
    # for instance in tenants:

    #     print(instance.name, instance.schema, instance.host)

    # tenants_list = [Tenant(**tenant.__dict__) for tenant in tenants]

    return {"name": "John Doe", "email": ""}


class TenantInfo(BaseModel):
    name: str
    schema: str
    host: str


@app.get("/tenant", response_model=TenantInfo)
def get_current_tenant(tenant: Tenant = Depends(get_tenant)):
    """Get the current tenant"""
    return tenant


@app.post("/tenant", response_model=TenantInfo)
def create_tenant(tenant: TenantInfo):
    tenant_create(tenant.name, tenant.schema, tenant.host)

    # new_tenant = Tenant(
    #     name=tenant.name,
    #     schema=tenant.schema,
    #     host=tenant.host,
    #     status=tenant.status,
    # )

    # db = SessionLocal()
    # db.add(new_tenant)
    # db.commit()
    # db.refresh(new_tenant)
    # db.close()
    # return new_tenant


def tenant_create(name: str, schema: str, host: str) -> None:
    """Before adding a new tenant, check if the database is up-to-date with migrations.

    Note:
    To add all the tables to the new schema, we need to create a new metadata object and add all the tables to it. OR we can runmigrations on the new schema
    to make it up to date with the other schemas
    """
    # Open a database connection using a context manager
    # connect to the correct schema # NOTE all addition to the database need to be given the correct schema
    # TODO: read the host and check if its in the shared schema tenants table and then proced tp allo wany changes to the database
    with with_db(schema) as db:
        # Load Alembic configuration and create Alembic context
        alembic_config = Config("alembic.ini")
        context = MigrationContext.configure(db.connection())
        script = alembic.script.ScriptDirectory.from_config(alembic_config)

        # Check if the database is up-to-date with migrations
        if context.get_current_revision() != script.get_current_head():
            raise RuntimeError("Database is not up-to-date. Execute migrations before adding new tenants.")

        import sys

        print(f"\n{sys._getframe().f_lineno}-{__name__}=====> \033[93mDatabase is up-to-date\033[0m\n")

        # If the database is up-to-date, add the new tenant
        tenant = Tenant(
            name=name,
            host=host,
            schema=schema,
            status=Status.active,
        )
        db.add(tenant)

        db.execute(sa.schema.CreateSchema(schema))

        get_tenant_specific_metadata().create_all(bind=db.connection())

        db.commit()


# -----------------------------------------------------

# TODO: add migrations and see if the code workds use pip env to have a master oommand for eacht enant and then run the migrations on each tenant
# use fuff
# add login and sue useypes to restict adding new tenets to pubic
# create a migration scrip that onyl runs on a flag- check chatgtp - to add users to the database and then run the migration on the new schema
