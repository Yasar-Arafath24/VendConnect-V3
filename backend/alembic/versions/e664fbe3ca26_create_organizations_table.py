"""create organizations table

Revision ID: e664fbe3ca26
Revises: 
Create Date: 2026-08-01 16:11:02.658549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e664fbe3ca26'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "organizations",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organization_code", sa.String(20), nullable=False),
        sa.Column("organization_name", sa.String(150), nullable=False),
        sa.Column("owner_name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(120), nullable=False),
        sa.Column("phone", sa.String(20), nullable=False),
        sa.Column("gst_number", sa.String(30), nullable=True),
        sa.Column("address", sa.String(500), nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("state", sa.String(100), nullable=True),
        sa.Column("pincode", sa.String(10), nullable=True),
        sa.Column("logo_url", sa.String(500), nullable=True),
        sa.Column(
            "subscription_plan",
            sa.String(20),
            server_default=sa.text("'FREE'"),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
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
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("organization_code"),
    )
    op.create_index(
        "ix_organizations_organization_code",
        "organizations",
        ["organization_code"],
    )
    op.create_index(
        "ix_organizations_organization_name",
        "organizations",
        ["organization_name"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_organizations_organization_name", table_name="organizations")
    op.drop_index("ix_organizations_organization_code", table_name="organizations")
    op.drop_table("organizations")
