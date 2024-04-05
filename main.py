from fastapi import FastAPI

from app.api.tenant.router import router as tenant_router
from app.api.user.router import router as user_router

app = FastAPI()

app.include_router(
    tenant_router,
    tags=["tenant"],
    prefix="/v1",
)

app.include_router(
    user_router,
    tags=["user"],
    prefix="/v1",
)
