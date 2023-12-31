"""added unique to que and theme

Revision ID: 0a3d2cc968ce
Revises: 99cecf80b4ca
Create Date: 2023-09-09 20:30:31.912596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a3d2cc968ce'
down_revision = '99cecf80b4ca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'questions', ['title'])
    op.create_unique_constraint(None, 'themes', ['title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'themes', type_='unique')
    op.drop_constraint(None, 'questions', type_='unique')
    # ### end Alembic commands ###
