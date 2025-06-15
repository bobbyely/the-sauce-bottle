"""create statement table

Revision ID: a5aa5ace5516
Revises: b335ac7d5b3f
Create Date: 2025-06-15 21:21:06.170524

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a5aa5ace5516'
down_revision = 'b335ac7d5b3f'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'statements',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('date_made', sa.Date(), nullable=True),
        sa.Column('politician_id', sa.Integer(), sa.ForeignKey('politicians.id'), nullable=False),
        sa.Column('ai_summary', sa.Text(), nullable=True),
        sa.Column('ai_contradiction_analysis', sa.Text(), nullable=True),
        sa.Column('source_url', sa.String(length=1024), nullable=True),
        sa.Column('source_type', sa.String(length=50), nullable=True),
        sa.Column('source_name', sa.String(length=255), nullable=True),
        sa.Column('review_status', sa.String(length=50), server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), onupdate=sa.text('now()')),
    )

def downgrade():
    op.drop_table('statements')