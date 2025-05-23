"""add_question_technology2

Revision ID: 3c41945c1670
Revises: 8731a349383d
Create Date: 2024-12-14 11:28:51.048810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c41945c1670'
down_revision: Union[str, None] = '8731a349383d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question_technology',
    sa.Column('question_id', sa.BigInteger(), nullable=False),
    sa.Column('technology_id', sa.BigInteger(), nullable=False),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], name=op.f('fk_question_technology_question_id_question')),
    sa.ForeignKeyConstraint(['technology_id'], ['technology.id'], name=op.f('fk_question_technology_technology_id_technology')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_question_technology')),
    sa.UniqueConstraint('id', name=op.f('uq_question_technology_id')),
    sa.UniqueConstraint('question_id', 'technology_id', name=op.f('uq_question_technology_question_id_technology_id'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question_technology')
    # ### end Alembic commands ###
