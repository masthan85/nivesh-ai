"""initial production-oriented schema

Revision ID: 20260926_01
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = '20260926_01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_pw', sa.String(length=255), nullable=False),
        sa.Column('risk', sa.String(length=20), nullable=True),
        sa.Column('horizon', sa.Integer(), nullable=True),
        sa.Column('monthly_sip', sa.Numeric(24, 2), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table(
        'holdings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('symbol', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('qty', sa.Numeric(24, 8), nullable=False),
        sa.Column('avg_price', sa.Numeric(24, 4), nullable=False),
        sa.Column('sector', sa.String(length=50), nullable=True),
        sa.Column('exchange', sa.String(length=10), nullable=True),
        sa.Column('asset_type', sa.String(length=20), nullable=True),
        sa.Column('buy_date', sa.String(length=20), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('user_id', 'symbol', 'exchange', name='uq_holding_user_symbol_exchange'),
    )
    op.create_index('ix_holdings_id', 'holdings', ['id'])

    op.create_table(
        'goals',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('icon', sa.String(length=10), nullable=True),
        sa.Column('target', sa.Numeric(24, 2), nullable=False),
        sa.Column('saved', sa.Numeric(24, 2), nullable=True),
        sa.Column('monthly', sa.Numeric(24, 2), nullable=False),
        sa.Column('years', sa.Integer(), nullable=False),
        sa.Column('risk', sa.String(length=20), nullable=True),
        sa.Column('color', sa.String(length=10), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_goals_id', 'goals', ['id'])

    op.create_table(
        'watchlist',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('symbol', sa.String(length=20), nullable=False),
        sa.Column('target', sa.Numeric(24, 4), nullable=True),
        sa.Column('stop_loss', sa.Numeric(24, 4), nullable=True),
        sa.Column('notes', sa.String(length=500), nullable=True),
        sa.Column('added_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('user_id', 'symbol', name='uq_watchlist_user_symbol'),
    )
    op.create_index('ix_watchlist_id', 'watchlist', ['id'])

    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('symbol', sa.String(length=20), nullable=False),
        sa.Column('alert_type', sa.String(length=10), nullable=False),
        sa.Column('price', sa.Numeric(24, 4), nullable=False),
        sa.Column('notify_push', sa.Boolean(), nullable=True),
        sa.Column('notify_email', sa.Boolean(), nullable=True),
        sa.Column('status', sa.String(length=10), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('triggered_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_alerts_id', 'alerts', ['id'])

    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('role', sa.String(length=10), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_chat_messages_id', 'chat_messages', ['id'])

    op.create_table(
        'audit_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('event_type', sa.String(length=80), nullable=False),
        sa.Column('outcome', sa.String(length=20), nullable=False),
        sa.Column('request_id', sa.String(length=64), nullable=True),
        sa.Column('ip_address', sa.String(length=64), nullable=True),
        sa.Column('metadata_json', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_audit_events_user_id', 'audit_events', ['user_id'])
    op.create_index('ix_audit_events_event_type', 'audit_events', ['event_type'])
    op.create_index('ix_audit_events_request_id', 'audit_events', ['request_id'])
    op.create_index('ix_audit_events_created_at', 'audit_events', ['created_at'])


def downgrade() -> None:
    for table in ['audit_events', 'chat_messages', 'alerts', 'watchlist', 'goals', 'holdings', 'users']:
        op.drop_table(table)
