"""Add_text_in_admin_model

Revision ID: 2b6e934e112b
Revises: 7fb637e8fce0
Create Date: 2024-06-04 16:28:15.835656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b6e934e112b'
down_revision = '7fb637e8fce0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=512),
               type_=sa.Text(length=512),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.Text(length=512),
               type_=sa.VARCHAR(length=512),
               existing_nullable=True)

    # ### end Alembic commands ###