"""empty message

Revision ID: 485450fc3387
Revises: 
Create Date: 2017-03-12 12:05:53.444280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '485450fc3387'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usertags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weibotags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('created_time', sa.Integer(), nullable=True),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('note', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('intro', sa.String(), nullable=True),
    sa.Column('tag_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['tag_id'], ['usertags.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cfavorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_time', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('weibo_id', sa.Integer(), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('follows',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    op.create_table('wcollects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_time', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('weibo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weibos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('created_time', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('comments_num', sa.Integer(), nullable=True),
    sa.Column('fav_num', sa.Integer(), nullable=True),
    sa.Column('col_num', sa.Integer(), nullable=True),
    sa.Column('cite_num', sa.Integer(), nullable=True),
    sa.Column('has_cite', sa.Boolean(), nullable=True),
    sa.Column('cite_id', sa.Integer(), nullable=True),
    sa.Column('origin_w_id', sa.Integer(), nullable=True),
    sa.Column('is_hidden', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['tag_id'], ['weibotags.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wfavorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_time', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('weibo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('created_time', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('weibo_id', sa.Integer(), nullable=True),
    sa.Column('fav_num', sa.Integer(), nullable=True),
    sa.Column('chat_num', sa.Integer(), nullable=True),
    sa.Column('is_hidden', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['weibo_id'], ['weibos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('commentchats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('created_time', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('weibo_id', sa.Integer(), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.Column('fav_num', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('commentchats')
    op.drop_table('comments')
    op.drop_table('wfavorites')
    op.drop_table('weibos')
    op.drop_table('wcollects')
    op.drop_table('follows')
    op.drop_table('cfavorites')
    op.drop_table('users')
    op.drop_table('weibotags')
    op.drop_table('usertags')
    # ### end Alembic commands ###
