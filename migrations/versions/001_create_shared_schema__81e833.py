"""001_create_shared_schema

Revision ID: 81e83351e712
Revises:
Create Date: 2024-04-14 18:17:01.148720

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "81e83351e712"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS shared")


def downgrade() -> None:
    # op.execute("DROP SCHEMA IF EXISTS shared CASCADE")
    pass
