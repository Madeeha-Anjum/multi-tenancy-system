from pydantic import BaseModel


class TenantInfo(BaseModel):
    name: str
    schema: str
    host: str
