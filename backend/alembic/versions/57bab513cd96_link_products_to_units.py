"""link products to units

Replace the free-text products.unit column with a unit_id
foreign key referencing units.id (ON DELETE SET NULL).

Revision ID: 57bab513cd96
Revises: e3ecad44e874
Create Date: 2026-08-05 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57bab513cd96'
down_revision: Union[str, Sequence[str], None] = 'e3ecad44e874'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'products',
        sa.Column('unit_id', sa.String(length=36), nullable=True),
    )
    op.create_foreign_key(
        'products_unit_id_fkey',
        'products',
        'units',
        ['unit_id'],
        ['id'],
        ondelete='SET NULL',
    )
    op.create_index(
        op.f('ix_products_unit_id'),
        'products',
        ['unit_id'],
        unique=False,
    )
    op.drop_column('products', 'unit')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        'products',
        sa.Column('unit', sa.String(length=50), nullable=False),
    )
    op.drop_index(op.f('ix_products_unit_id'), table_name='products')
    op.drop_constraint('products_unit_id_fkey', 'products', type_='foreignkey')
    op.drop_column('products', 'unit_id')
