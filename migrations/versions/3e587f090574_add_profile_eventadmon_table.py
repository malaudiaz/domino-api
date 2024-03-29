"""add profile eventadmon table

Revision ID: 3e587f090574
Revises: 2458f7de0b07
Create Date: 2023-08-10 13:11:57.485981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e587f090574'
down_revision = '2458f7de0b07'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ext_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ext_code', sa.String(length=10), nullable=False),
    sa.Column('type_file', sa.String(length=10), nullable=False),
    sa.Column('created_by', sa.String(length=50), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ext_code'),
    schema='resources'
    )
    op.create_table('profile_event_admon',
    sa.Column('profile_id', sa.String(), nullable=False),
    sa.Column('updated_by', sa.String(), nullable=False),
    sa.Column('updated_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['enterprise.profile_member.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['enterprise.users.username'], ),
    sa.PrimaryKeyConstraint('profile_id'),
    schema='enterprise'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profile_event_admon', schema='enterprise')
    op.drop_table('ext_types', schema='resources')
    # ### end Alembic commands ###
