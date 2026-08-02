"""add id and assigned_at to user_roles

Revision ID: d165946b74d8
Revises: 4ad4d2a2e737
Create Date: 2026-08-02 17:52:15.153257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd165946b74d8'
down_revision: Union[str, Sequence[str], None] = '4ad4d2a2e737'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {
        col["name"]
        for col in inspector.get_columns("user_roles")
    }

    if "id" not in columns:
        op.add_column(
            "user_roles",
            sa.Column(
                "id",
                sa.String(36),
                server_default=sa.text("gen_random_uuid()::text"),
                nullable=False,
            ),
        )

    if "assigned_at" not in columns:
        op.add_column(
            "user_roles",
            sa.Column(
                "assigned_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
        )

    # Replace composite PK (user_id, role_id) with id PK
    op.drop_constraint(
        "user_roles_pkey",
        "user_roles",
        type_="primary",
    )
    op.create_primary_key(
        "user_roles_pkey",
        "user_roles",
        ["id"],
    )

    # Keep (user_id, role_id) unique
    op.create_unique_constraint(
        "uq_user_roles_user_role",
        "user_roles",
        ["user_id", "role_id"],
    )

    # Remove backfill default so the column matches the model
    op.alter_column(
        "user_roles",
        "id",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {
        col["name"]
        for col in inspector.get_columns("user_roles")
    }

    op.drop_constraint(
        "uq_user_roles_user_role",
        "user_roles",
        type_="unique",
    )
    op.drop_constraint(
        "user_roles_pkey",
        "user_roles",
        type_="primary",
    )
    op.create_primary_key(
        "user_roles_pkey",
        "user_roles",
        ["user_id", "role_id"],
    )

    if "assigned_at" in columns:
        op.drop_column("user_roles", "assigned_at")

    if "id" in columns:
        op.drop_column("user_roles", "id")
