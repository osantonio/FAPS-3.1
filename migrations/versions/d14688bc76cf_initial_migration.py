"""initial migration

Revision ID: d14688bc76cf
Revises: 
Create Date: 2024-01-11 23:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd14688bc76cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Crear tabla store_type
    op.create_table('store_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('can_distribute_to_beneficiaries', sa.Boolean(), nullable=True),
        sa.Column('can_distribute_to_store', sa.Boolean(), nullable=True),
        sa.Column('can_distribute_to_warehouse', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id', name='pk_store_type')
    )
    
    # Crear tabla supply si no existe
    op.create_table('supply',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('entry_date', sa.Date(), nullable=False),
        sa.Column('photo', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('store_type_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['store_type_id'], ['store_type.id'], name='fk_supply_store_type'),
        sa.PrimaryKeyConstraint('id', name='pk_supply')
    )


def downgrade():
    op.drop_table('supply')
    op.drop_table('store_type')
