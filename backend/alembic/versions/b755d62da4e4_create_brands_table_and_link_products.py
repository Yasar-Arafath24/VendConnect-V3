"""create brands table and link products to brands

Revision ID: b755d62da4e4
Revises: 19f9763f48dd
Create Date: 2026-08-05 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b755d62da4e4'
down_revision: Union[str, Sequence[str], None] = '19f9763f48dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'brands',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('organization_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('logo_url', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_brands_id'), 'brands', ['id'], unique=False)
    op.create_index(op.f('ix_brands_name'), 'brands', ['name'], unique=False)
    op.create_index(op.f('ix_brands_organization_id'), 'brands', ['organization_id'], unique=False)

    bind = op.get_bind()
    fk_names = [
        fk["name"]
        for fk in sa.inspect(bind).get_foreign_keys("products")
    ]

    if "products_brand_id_fkey" not in fk_names:
        with op.batch_alter_table('products') as batch_op:
            batch_op.create_foreign_key(
                'products_brand_id_fkey',
                'brands',
                ['brand_id'],
                ['id'],
                ondelete='SET NULL',
            )
    op.create_index(
        op.f('ix_products_brand_id'),
        'products',
        ['brand_id'],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_products_brand_id'), table_name='products')

    bind = op.get_bind()
    fk_names = [
        fk["name"]
        for fk in sa.inspect(bind).get_foreign_keys("products")
    ]

    if "products_brand_id_fkey" in fk_names:
        with op.batch_alter_table('products') as batch_op:
            batch_op.drop_constraint(
                'products_brand_id_fkey',
                type_='foreignkey',
            )

    op.drop_index(op.f('ix_brands_organization_id'), table_name='brands')
    op.drop_index(op.f('ix_brands_name'), table_name='brands')
    op.drop_index(op.f('ix_brands_id'), table_name='brands')
    op.drop_table('brands')
