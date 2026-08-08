"""create inventory table

Revision ID: 88256b642540
Revises: 7800aabd2fd7
Create Date: 2026-08-07 16:40:40.655923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88256b642540'
down_revision: Union[str, Sequence[str], None] = '7800aabd2fd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    if sa.inspect(op.get_bind()).has_table("inventory"):
        return

    op.create_table(
        'inventory',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('organization_id', sa.String(), nullable=False),
        sa.Column('warehouse_id', sa.String(), nullable=False),
        sa.Column('product_id', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('reserved_quantity', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('reorder_level', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('max_stock_level', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('organization_id', 'warehouse_id', 'product_id', name='uq_inventory_product_warehouse')
    )
    op.create_index(op.f('ix_inventory_id'), 'inventory', ['id'], unique=False)
    op.create_index(op.f('ix_inventory_organization_id'), 'inventory', ['organization_id'], unique=False)
    op.create_index(op.f('ix_inventory_warehouse_id'), 'inventory', ['warehouse_id'], unique=False)
    op.create_index(op.f('ix_inventory_product_id'), 'inventory', ['product_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_inventory_product_id'), table_name='inventory')
    op.drop_index(op.f('ix_inventory_warehouse_id'), table_name='inventory')
    op.drop_index(op.f('ix_inventory_organization_id'), table_name='inventory')
    op.drop_index(op.f('ix_inventory_id'), table_name='inventory')
    op.drop_table('inventory')
