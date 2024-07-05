from pydantic import BaseModel


class TenantInfo(BaseModel):
    tenant_schema_name: str
    sub_domain: str
