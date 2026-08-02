"""create users and user_roles tables

Revision ID: a1b2c3d4e5f6
Revises: 9847afee3ae3
Create Date: 2026-08-02 10:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '9847afee3ae3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())

    # Users
    if "users" not in tables:
        op.create_table(
            "users",
            sa.Column("id", sa.String(36), nullable=False),
            sa.Column("organization_id", sa.String(36), nullable=False),
            sa.Column("first_name", sa.String(100), nullable=False),
            sa.Column("last_name", sa.String(100), nullable=False),
            sa.Column("email", sa.String(255), nullable=False),
            sa.Column("phone", sa.String(20), nullable=True),
            sa.Column("password_hash", sa.String(255), nullable=False),
            sa.Column("profile_image", sa.String(500), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("is_verified", sa.Boolean(), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.ForeignKeyConstraint(
                ["organization_id"],
                ["organizations.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("email"),
        )
        op.create_index(
            "ix_users_organization_id",
            "users",
            ["organization_id"],
        )
        op.create_index(
            "ix_users_email",
            "users",
            ["email"],
            unique=True,
        )

    # User <-> Role association table
    if "user_roles" not in tables:
        op.create_table(
            "user_roles",
            sa.Column("user_id", sa.String(36), nullable=False),
            sa.Column("role_id", sa.String(36), nullable=False),
            sa.ForeignKeyConstraint(
                ["role_id"],
                ["roles.id"],
                ondelete="CASCADE",
            ),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["users.id"],
                ondelete="CASCADE",
            ),
            sa.PrimaryKeyConstraint("user_id", "role_id"),
        )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())

    if "user_roles" in tables:
        op.drop_table("user_roles")

    if "users" in tables:
        op.drop_index("ix_users_email", table_name="users")
        op.drop_index("ix_users_organization_id", table_name="users")
        op.drop_table("users")
