from fastapi import FastAPI

from multi_tenancy_system.api import tenant

app = FastAPI()

app.include_router(
    tenant.routes,
    tags=["tenant"],
    prefix="/v1",
)
