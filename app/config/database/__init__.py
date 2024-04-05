from contextlib import contextmanager
from typing import Optional

from fastapi import Depends, HTTPException, Request
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from app.models import Base, Tenant

from .engine import engine

__all__ = ["get_db", "get_tenant", "with_db", "get_tenant_specific_metadata"]


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

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
