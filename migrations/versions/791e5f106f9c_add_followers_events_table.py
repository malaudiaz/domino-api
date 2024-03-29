"""add followers events table

Revision ID: 791e5f106f9c
Revises: 388f553b4347
Create Date: 2023-11-04 08:35:26.960248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '791e5f106f9c'
down_revision = '388f553b4347'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events_followers',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('profile_id', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('element_type', sa.String(length=30), nullable=False),
    sa.Column('element_id', sa.String(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.Column('created_date', sa.Date(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['enterprise.profile_member.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('profile_id'),
    schema='events'
    )
    
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('events_followers', schema='events')
    # ### end Alembic commands ###
