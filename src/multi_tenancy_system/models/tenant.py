from enum import Enum

import sqlalchemy as sa

from .base import Base


class TenantStatuses(Enum):
    active = "active"
    inactive = "inactive"


class Tenant(Base):
    __tablename__ = "tenants"
    __table_args__ = ({"schema": "shared"},)

    tenant_id = sa.Column(
        "tenant_id",
        sa.Integer,
        primary_key=True,
        nullable=False,
        comment="The unique identifier for the tenant",
    )

    tenant_schema_name = sa.Column(
        "tenant_schema_name",
        sa.String(256),
        nullable=False,
        unique=True,
        comment="The schema for the database of the tenant example: site1",
    )

    sub_domain = sa.Column(
        "sub_domain",
        sa.String(256),
        nullable=False,
        index=True,
        unique=True,
        comment="the name of the tenant example: site1",
    )

    current_status = sa.Column(
        "current_status",
        # inherit_schema=True will place the enum in the correct schema and not in the public schema
        sa.Enum(TenantStatuses, inherit_schema=True),
        nullable=False,
        comment="The status of the tenant",
    )
