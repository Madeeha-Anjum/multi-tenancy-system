"""003_create_tenants_table

Revision ID: 5fae0a5b6c8c
Revises: 6c588759fb5e
Create Date: 2024-04-14 19:13:04.675819
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5fae0a5b6c8c"
down_revision: Union[str, None] = "81e83351e712"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS shared")

    op.create_table(
        "tenants",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
            comment="The unique identifier for the tenant",
        ),
        sa.Column(
            "name",
            sa.String(length=256),
            nullable=False,
            comment="the name of the tenant example: site1",
        ),
        sa.Column(
            "schema",
            sa.String(length=256),
            nullable=False,
            comment="The schema for the database of the tenant example: site1",
        ),
        sa.Column(
            "host",
            sa.String(length=256),
            nullable=False,
            comment="The host of the tenant example: site1.localhost",
        ),
        sa.Column(
            "status",
            sa.Enum(
                "active",
                "inactive",
                name="status",
                schema="shared",
                inherit_schema=True,
            ),
            nullable=False,
            comment="The status of the tenant",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tenants")),
        sa.UniqueConstraint("host", name=op.f("uq_tenants_host")),
        sa.UniqueConstraint("schema", name=op.f("uq_tenants_schema")),
        schema="shared",
    )
    op.create_index(op.f("ix_tenants_name"), "tenants", ["name"], unique=True, schema="shared")


def downgrade() -> None:
    op.drop_index(op.f("ix_tenants_name"), table_name="tenants", schema="shared")
    # op.drop_table("tenants", schema="shared")
