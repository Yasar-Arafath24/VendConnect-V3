"""create rbac tables

Revision ID: 9847afee3ae3
Revises: 568476ca99b8
Create Date: 2026-08-02 09:30:58.026875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9847afee3ae3'
down_revision: Union[str, Sequence[str], None] = '568476ca99b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())

    # Roles
    if "roles" not in tables:
        op.create_table(
            "roles",
            sa.Column("id", sa.String(36), nullable=False),
            sa.Column("name", sa.String(100), nullable=False),
            sa.Column("description", sa.String(255), nullable=True),
            sa.Column("organization_id", sa.String(36), nullable=True),
            sa.Column(
                "is_system",
                sa.Boolean(),
                server_default=sa.text("false"),
                nullable=False,
            ),
            sa.ForeignKeyConstraint(
                ["organization_id"],
                ["organizations.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )

    # Permissions
    if "permissions" not in tables:
        op.create_table(
            "permissions",
            sa.Column("id", sa.String(36), nullable=False),
            sa.Column("key", sa.String(100), nullable=False),
            sa.Column("resource", sa.String(50), nullable=False),
            sa.Column("action", sa.String(50), nullable=False),
            sa.Column("description", sa.String(255), nullable=True),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("key"),
        )
        op.create_index(
            "ix_permissions_key",
            "permissions",
            ["key"],
            unique=True,
        )

    # Many-to-many association table
    if "role_permissions" not in tables:
        op.create_table(
            "role_permissions",
            sa.Column("role_id", sa.String(36), nullable=False),
            sa.Column("permission_id", sa.String(36), nullable=False),
            sa.ForeignKeyConstraint(
                ["permission_id"],
                ["permissions.id"],
                ondelete="CASCADE",
            ),
            sa.ForeignKeyConstraint(
                ["role_id"],
                ["roles.id"],
                ondelete="CASCADE",
            ),
            sa.PrimaryKeyConstraint("role_id", "permission_id"),
        )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())

    if "role_permissions" in tables:
        op.drop_table("role_permissions")

    if "permissions" in tables:
        op.drop_index(
            "ix_permissions_key",
            table_name="permissions",
        )
        op.drop_table("permissions")

    if "roles" in tables:
        op.drop_table("roles")
