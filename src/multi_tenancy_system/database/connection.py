from contextlib import contextmanager
from typing import Optional

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from multi_tenancy_system.models.tenant import Tenant

from .engine import engine

__all__ = ["get_default_db_session", "get_tenant_db_session"]


def get_sub_domain_from_request(req: Request) -> str:
    """Get the subdomain from the request
    For example, if the request is for "tenant1.example.com",
    this function will return "tenant1" """
    return (req.headers["host"].split(":", 1)[0]).split(".")[-2]


def get_default_db_session():
    return with_default_db()


def get_tenant_db_session(tenant_schema_name=Depends(get_sub_domain_from_request)):
    # check if tenant exists in the "shared" schema
    with with_default_db() as db:
        tenant = db.query(Tenant).filter(Tenant.sub_domain == tenant_schema_name).one_or_none()

    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return with_tenant_db(tenant_schema=tenant_schema_name)


@contextmanager
def with_default_db():
    """Get a database connection using the schemas defined in each model"""
    connectable = engine.execution_options()
    try:
        db = Session(autocommit=False, autoflush=False, bind=connectable)
        yield db
    finally:
        db.close()


@contextmanager
def with_tenant_db(tenant_schema: Optional[str]):
    """Get a database connection for the given tenant schema"""
    connectable = engine.execution_options(schema_translate_map={"tenant": tenant_schema})

    try:
        db = Session(autocommit=False, autoflush=False, bind=connectable)
        yield db
    finally:
        db.close()
