# DARK8 OS - Database Migrations
"""
Alembic database migration setup.
"""

from alembic import op
import sqlalchemy as sa


def upgrade():
    """Upgrade database schema"""
    
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), unique=True, nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('path', sa.String(1024), nullable=False),
        sa.Column('app_type', sa.String(50)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
        sa.Column('metadata', sa.JSON()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_input', sa.Text(), nullable=False),
        sa.Column('ai_response', sa.Text(), nullable=False),
        sa.Column('intent', sa.String(100)),
        sa.Column('confidence', sa.Float()),
        sa.Column('entities', sa.JSON()),
        sa.Column('context', sa.JSON()),
        sa.Column('timestamp', sa.DateTime()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('intent', sa.String(100)),
        sa.Column('status', sa.String(20)),
        sa.Column('result', sa.Text()),
        sa.Column('parameters', sa.JSON()),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('completed_at', sa.DateTime()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create knowledge_base table
    op.create_table(
        'knowledge_base',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(50)),
        sa.Column('title', sa.String(255)),
        sa.Column('content', sa.Text()),
        sa.Column('language', sa.String(50)),
        sa.Column('tags', sa.JSON()),
        sa.Column('embedding', sa.String(4096)),
        sa.Column('created_at', sa.DateTime()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create audit_log table
    op.create_table(
        'audit_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(100)),
        sa.Column('user_input', sa.Text()),
        sa.Column('parameters', sa.JSON()),
        sa.Column('result', sa.String(20)),
        sa.Column('error_message', sa.Text()),
        sa.Column('timestamp', sa.DateTime()),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    """Downgrade database schema"""
    op.drop_table('audit_log')
    op.drop_table('knowledge_base')
    op.drop_table('tasks')
    op.drop_table('conversations')
    op.drop_table('projects')
