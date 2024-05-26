from contextlib import contextmanager
from typing import Optional

from fastapi import Depends, HTTPException, Request
from multi_tenancy_system.models.base import Base
from multi_tenancy_system.models.tenant import Tenant
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from .engine import engine

# automattically get the tenant from the request header based on host and port and return corredct db session


def get_tenant_specific_metadata():
    meta = MetaData(schema="tenant_default")
    for table in Base.metadata.tables.values():
        if table.schema == "tenant_default":
            table.tometadata(meta)
    return meta


# ------------------------------------------------------------------------------------------------------


def get_sub_domain_from_request(req: Request) -> str:
    # eacmple
    # google.localhost:8000
    # fun.google.localhost:8000
    fqdn = (req.headers["host"].split(":", 1)[0]).split(".")[-2]
    return fqdn


def get_default_db_namespace_session(sub_domain=Depends(get_sub_domain_from_request)):
    return with_default_db_namespace()


def get_tenant_db_namespace_session(tenant_schema_name=Depends(get_sub_domain_from_request)):
    # check if tenant exists in the "shared" schema
    with with_default_db_namespace() as db:
        tenant = db.query(Tenant).filter(Tenant.sub_domain == tenant_schema_name).one_or_none()

    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return with_db_namespace(tenant_schema=tenant_schema_name)


@contextmanager
def with_default_db_namespace():
    connectable = engine.execution_options()
    try:
        db = Session(autocommit=False, autoflush=False, bind=connectable)
        yield db
    finally:
        db.close()


@contextmanager
def with_db_namespace(tenant_schema: Optional[str]):
    """Get a database connection for the given tenant schema"""

    schema_translate_map = dict(tenant=tenant_schema)

    connectable = engine.execution_options(schema_translate_map=schema_translate_map)

    try:
        db = Session(autocommit=False, autoflush=False, bind=connectable)
        yield db
    finally:
        db.close()
