import sqlalchemy as sa
from alembic.config import Config
from alembic.migration import MigrationContext
from fastapi import APIRouter, Depends

import migrations
from app.config.database import get_tenant, get_tenant_specific_metadata, with_db
from app.models.tenant import Tenant, TenantStatus

from .schema import TenantInfo

router = APIRouter(
    tags=["tenant"],
    prefix="/tenant",
)


@router.get("/", response_model=TenantInfo)
def get_current_tenant(tenant: Tenant = Depends(get_tenant)):
    """Get the current tenant"""
    return tenant


@router.post("/", response_model=TenantInfo)
def create_tenant(tenant: TenantInfo):
    tenant_create(tenant.name, tenant.schema, tenant.host)


def tenant_create(name: str, schema: str, host: str) -> None:
    """Before adding a new tenant, check if the database is up-to-date with migrations.

    Note:
    To add all the tables to the new schema, we need to create a new metadata object and add all the tables to it. OR we can runmigrations on the new schema
    to make it up to date with the other schemas
    """
    # Open a database connection using a context manager
    # connect to the correct schema # NOTE all addition to the database need to be given the correct schema
    # TODO: read the host and check if its in the shared schema tenants table and then proced tp allo wany changes to the database
    with with_db(schema) as db:
        # Load Alembic configuration and create Alembic context
        alembic_config = Config("alembic.ini")
        context = MigrationContext.configure(db.connection())
        script = migrations.script.ScriptDirectory.from_config(alembic_config)

        # Check if the database is up-to-date with migrations
        if context.get_current_revision() != script.get_current_head():
            raise RuntimeError("Database is not up-to-date. Execute migrations before adding new tenants.")

        import sys

        print(f"\n{sys._getframe().f_lineno}-{__name__}=====> \033[93mDatabase is up-to-date\033[0m\n")

        # If the database is up-to-date, add the new tenant
        tenant = Tenant(
            name=name,
            host=host,
            schema=schema,
            status=TenantStatus.active,
        )
        db.add(tenant)

        db.execute(sa.schema.CreateSchema(schema))

        get_tenant_specific_metadata().create_all(bind=db.connection())

        db.commit()


# -----------------------------------------------------

# TODO: add migrations and see if the code workds use pip env to have a master oommand for eacht enant and then run the migrations on each tenant
# use fuff
# add login and sue useypes to restict adding new tenets to pubic
# create a migration scrip that onyl runs on a flag- check chatgtp - to add users to the database and then run the migration on the new schema
