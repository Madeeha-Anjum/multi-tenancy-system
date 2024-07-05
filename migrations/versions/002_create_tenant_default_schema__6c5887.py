"""002_create_tenant_default_schema

Revision ID: 6c588759fb5e
Revises: 81e83351e712
Create Date: 2024-04-14 18:17:01.148721

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6c588759fb5e"
down_revision: Union[str, None] = "81e83351e712"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # tables are created in the tenant_default schema if the tenants table is empty
    op.execute("CREATE SCHEMA IF NOT EXISTS tenant_default")


def downgrade() -> None:
    # op.execute("DROP SCHEMA IF EXISTS tenant_default CASCADE")
    pass
