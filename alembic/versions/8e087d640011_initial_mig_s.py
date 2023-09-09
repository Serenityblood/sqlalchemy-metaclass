"""Initial mig-s

Revision ID: 8e087d640011
Revises: 
Create Date: 2023-09-08 19:57:18.742877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e087d640011'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('themes',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('questions',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('theme_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['theme_id'], ['themes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answers',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=False),
    sa.Column('question_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answers')
    op.drop_table('questions')
    op.drop_table('themes')
    op.drop_table('admins')
    # ### end Alembic commands ###