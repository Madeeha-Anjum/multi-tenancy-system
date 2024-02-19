"""create_tenant_default_schema

Revision ID: 6c588759fb5e
Revises: 3869ced5bde1
Create Date: 2024-02-09 15:44:23.113597

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "6c588759fb5e"
down_revision: Union[str, None] = "3869ced5bde1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # tables are created in the tenant_default schema if the tenants table is empty
    op.execute("CREATE SCHEMA IF NOT EXISTS tenant_default")
    


def downgrade( ) -> None:
    op.execute("CREATE SCHEMA IF EXISTS tenant_default")