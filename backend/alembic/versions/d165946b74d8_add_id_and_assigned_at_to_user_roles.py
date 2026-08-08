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

    if bind.dialect.name == "postgresql":
        id_default = sa.text("gen_random_uuid()::text")
        assigned_at_default = sa.text("now()")
    else:
        id_default = sa.text("lower(hex(randomblob(16)))")
        assigned_at_default = sa.text("CURRENT_TIMESTAMP")

    with op.batch_alter_table("user_roles") as batch_op:
        if "id" not in columns:
            batch_op.add_column(
                sa.Column(
                    "id",
                    sa.String(36),
                    server_default=id_default,
                    nullable=False,
                ),
            )

        if "assigned_at" not in columns:
            batch_op.add_column(
                sa.Column(
                    "assigned_at",
                    sa.DateTime(timezone=True),
                    server_default=assigned_at_default,
                    nullable=False,
                ),
            )

        # Replace composite PK (user_id, role_id) with id PK
        if bind.dialect.name == "postgresql":
            batch_op.drop_constraint(
                "user_roles_pkey",
                type_="primary",
            )
        batch_op.create_primary_key(
            "user_roles_pkey",
            ["id"],
        )

        # Keep (user_id, role_id) unique
        batch_op.create_unique_constraint(
            "uq_user_roles_user_role",
            ["user_id", "role_id"],
        )

        # Remove backfill default so the column matches the model
        batch_op.alter_column(
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

    with op.batch_alter_table("user_roles") as batch_op:
        batch_op.drop_constraint(
            "uq_user_roles_user_role",
            type_="unique",
        )
        if bind.dialect.name == "postgresql":
            batch_op.drop_constraint(
                "user_roles_pkey",
                type_="primary",
            )
        batch_op.create_primary_key(
            "user_roles_pkey",
            ["user_id", "role_id"],
        )

        if "assigned_at" in columns:
            batch_op.drop_column("user_roles", "assigned_at")

        if "id" in columns:
            batch_op.drop_column("user_roles", "id")
