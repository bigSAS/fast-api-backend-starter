"""add user group table

Revision ID: 4ec184770d03
Revises: e619152902ba
Create Date: 2021-07-04 12:36:24.092957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ec184770d03'
down_revision = 'e619152902ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_groups_id'), 'user_groups', ['id'], unique=False)
    op.create_index(op.f('ix_user_groups_name'), 'user_groups', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_groups_name'), table_name='user_groups')
    op.drop_index(op.f('ix_user_groups_id'), table_name='user_groups')
    op.drop_table('user_groups')
    # ### end Alembic commands ###