from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from multi_tenancy_system.database import get_default_db_session, get_tenant_db_session
from multi_tenancy_system.models.tenant import Tenant
from sqlalchemy.orm import Session

from .schema import TenantInfo

routes = APIRouter(
    tags=["tenant"],
    prefix="/tenant",
)


@routes.get("/", response_model=TenantInfo)
def get_current_tenant(tenant: Tenant = Depends(get_default_db_session)):
    """Get the current tenant"""
    return JSONResponse(
        content=jsonable_encoder(tenant),
        status_code=200,
    )


@routes.post("/", response_model=TenantInfo)
def create_tenant(tenant: TenantInfo):
    """Create a new tenant"""
    create_tenant(tenant)
    return JSONResponse(
        content=jsonable_encoder(tenant),
        status_code=201,
    )


@routes.post("/x", response_model=TenantInfo)
def test(body: TenantInfo, db: Session = Depends(get_tenant_db_session)):
    # do stuff
    # go and fetch a list of candies from the db
    print("Hello Madeeha!")
    return body


# def get_tenant_db_namespace_session(Depends(get_subdomain_from_url)):
