import alembic
import sqlalchemy as sa
from alembic.config import Config
from alembic.migration import MigrationContext
from multi_tenancy_system.database.connection import with_db_namespace
from multi_tenancy_system.models.base import Base
from multi_tenancy_system.models.tenant import Tenant, TenantStatuses


def create_tenant(tenant_schema_name: str, sub_domain: str) -> None:
    """Create a new tenant in the shared schema tenants table and create the schema in the database.

    1. check if the database is up-to-date with migrations.
    2. add the new tenant.
    3. create the schema in the database.
    4. commit the transaction.
    """
    with with_db_namespace(tenant_schema_name) as db:
        # Load Alembic configuration and create Alembic context
        alembic_config = Config("alembic.ini")
        context = MigrationContext.configure(db.connection())
        script = alembic.script.ScriptDirectory.from_config(alembic_config)
        # Check if the database is up-to-date with migrations
        if context.get_current_revision() != script.get_current_head():
            raise RuntimeError("Database is not up-to-date. Execute migrations before adding new tenants.")

        # If the database is up-to-date, add the new tenant
        tenant = Tenant(
            sub_domain=sub_domain,
            tenant_schema_name=tenant_schema_name,
            current_status=TenantStatuses.active,
        )
        db.add(tenant)
        db.execute(sa.schema.CreateSchema(tenant_schema_name))
        get_tenant_specific_metadata().create_all(bind=db.connection())
        db.commit()


def get_tenant_specific_metadata():
    meta = sa.MetaData(schema="tenant_default")
    for table in Base.metadata.tables.values():
        if table.schema == "tenant_default":
            table.tometadata(meta)
    return meta
