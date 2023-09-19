"""empty message

Revision ID: e74c5d72638c
Revises: d08e0ffea0b1
Create Date: 2023-09-19 20:21:13.687047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e74c5d72638c'
down_revision = 'd08e0ffea0b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('starships', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('model',
               existing_type=sa.VARCHAR(length=60),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('manufacturer',
               existing_type=sa.VARCHAR(length=90),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('max_atmosphering_speed',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=60),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('starships', schema=None) as batch_op:
        batch_op.alter_column('max_atmosphering_speed',
               existing_type=sa.String(length=60),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)
        batch_op.alter_column('manufacturer',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=90),
               existing_nullable=False)
        batch_op.alter_column('model',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=60),
               existing_nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)

    # ### end Alembic commands ###