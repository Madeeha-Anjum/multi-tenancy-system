from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from multi_tenancy_system.database.connection import get_tenant
from multi_tenancy_system.models.tenant import Tenant

from .schema import TenantInfo

routes = APIRouter(
    tags=["tenant"],
    prefix="/tenant",
)

from multi_tenancy_system.database import connection

connection.get_tenant()


@routes.get("/", response_model=TenantInfo)
def get_current_tenant(tenant: Tenant = Depends(get_tenant)):
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
