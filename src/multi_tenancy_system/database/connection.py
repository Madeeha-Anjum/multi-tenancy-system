from contextlib import contextmanager
from typing import Optional

from fastapi import Depends, HTTPException, Request
from multi_tenancy_system.models.base import Base
from multi_tenancy_system.models.tenant import Tenant
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from .engine import engine


# automattically get the tenant from the request header based on host and port and return corredct db session
def get_tenant(req: Request) -> Tenant:
    """Get the tenant based on the request header"""
    subdomain = req.headers["host"].split(":", 1)[0]

    with with_db(None) as db:
        tenant = db.query(Tenant).filter(Tenant.domain_name == subdomain).one_or_none()

    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return tenant


def get_tenant_specific_metadata():
    meta = MetaData(schema="tenant_default")
    for table in Base.metadata.tables.values():
        if table.schema == "tenant_default":
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


# def get_db(self, tenant: Tenant = Depends(get_tenant)):
#     """Get the database session for the current tenant"""
#     with self.with_db(tenant.tenant_name) as db:
#         yield db  # returning the db and then completed when the function is done
