from enum import Enum

import sqlalchemy as sa

from .base import Base


class TenantStatus(Enum):
    active = "active"
    inactive = "inactive"


class Tenant(Base):
    # NOTE: we want tp place the tenants in the shared schema becase we dont want to use public becase
    # ALL tables that dont have a schema will be placed in the public schema, this way if any tables are missing a scema we will notice it
    __tablename__ = "tenants"
    __table_args__ = ({"schema": "shared"},)

    # add help text to the columns
    id = sa.Column(
        "id",
        sa.Integer,
        primary_key=True,
        nullable=False,
        comment="The unique identifier for the tenant",
    )
    name = sa.Column(
        "name",
        sa.String(256),
        nullable=False,
        index=True,
        unique=True,
        comment="the name of the tenant example: site1",
    )
    schema = sa.Column(
        "schema",
        sa.String(256),
        nullable=False,
        unique=True,
        comment="The schema for the database of the tenant example: site1",
    )
    host = sa.Column(
        "host",
        sa.String(256),
        nullable=False,
        unique=True,
        comment="The host of the tenant example: site1.localhost",
    )
    status = sa.Column(
        "status",
        # inherit_schema=True will place the enum in the correct schema and not in the public schema
        sa.Enum(TenantStatus, inherit_schema=True),
        nullable=False,
        comment="The status of the tenant",
    )
