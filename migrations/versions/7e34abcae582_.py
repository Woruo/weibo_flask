"""empty message

Revision ID: 7e34abcae582
Revises: 14fa482b0bb5
Create Date: 2017-03-14 14:41:09.970380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e34abcae582'
down_revision = '14fa482b0bb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weibos', sa.Column('only_friends', sa.Boolean(), nullable=True))
    op.add_column('weibos', sa.Column('only_self', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('weibos', 'only_self')
    op.drop_column('weibos', 'only_friends')
    # ### end Alembic commands ###