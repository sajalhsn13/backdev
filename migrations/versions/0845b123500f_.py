"""empty message

Revision ID: 0845b123500f
Revises: e5c9974659e7
Create Date: 2020-07-04 16:28:24.375700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0845b123500f'
down_revision = 'e5c9974659e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'posts', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'user_id')
    # ### end Alembic commands ###