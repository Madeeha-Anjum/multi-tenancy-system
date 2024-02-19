"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

from migrations.tenant import for_each_tenant_schema

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}

@for_each_tenant_schema
def upgrade(schema: str) -> None:
    preparer = sa.sql.compiler.IdentifierPreparer(op.get_bind().dialect)
    schema_quoted = preparer.format_schema(schema) #  used in queries like op.execute(f"DROP TYPE {schema_quoted}.myenum")
    
    ${upgrades if upgrades else "pass"}

@for_each_tenant_schema
def downgrade(schema: str) -> None:
    preparer = sa.sql.compiler.IdentifierPreparer(op.get_bind().dialect)
    schema_quoted = preparer.format_schema(schema)
    
    ${downgrades if downgrades else "pass"}
