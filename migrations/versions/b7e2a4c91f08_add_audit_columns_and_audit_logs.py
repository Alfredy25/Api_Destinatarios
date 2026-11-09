"""add audit columns and audit logs

Revision ID: b7e2a4c91f08
Revises: 7cdb1799f320
Create Date: 2026-11-09 11:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7e2a4c91f08'
down_revision: Union[str, Sequence[str], None] = '7cdb1799f320'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _add_audit_columns(table: str, include_created_at: bool) -> None:
    if include_created_at:
        op.add_column(
            table,
            sa.Column(
                'created_at',
                sa.DateTime(timezone=True),
                server_default=sa.text('now()'),
                nullable=False,
            ),
        )
    op.add_column(
        table,
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
    )
    op.add_column(table, sa.Column('created_by', sa.Integer(), nullable=True))
    op.add_column(table, sa.Column('updated_by', sa.Integer(), nullable=True))
    op.create_foreign_key(
        f'fk_{table}_created_by_users',
        table,
        'users',
        ['created_by'],
        ['id'],
    )
    op.create_foreign_key(
        f'fk_{table}_updated_by_users',
        table,
        'users',
        ['updated_by'],
        ['id'],
    )


def _drop_audit_columns(table: str, include_created_at: bool) -> None:
    op.drop_constraint(f'fk_{table}_updated_by_users', table, type_='foreignkey')
    op.drop_constraint(f'fk_{table}_created_by_users', table, type_='foreignkey')
    op.drop_column(table, 'updated_by')
    op.drop_column(table, 'created_by')
    op.drop_column(table, 'updated_at')
    if include_created_at:
        op.drop_column(table, 'created_at')


def upgrade() -> None:
    """Upgrade schema."""
    tables_with_created_at = (
        'addresses',
        'contacts',
        'job_roles',
        'organizations',
        'positions',
        'titles',
        'volantes',
    )
    for table in tables_with_created_at:
        _add_audit_columns(table, include_created_at=True)

    # receivers ya tiene created_at
    _add_audit_columns('receivers', include_created_at=False)

    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('entity_name', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column(
            'changed_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('changes', sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_audit_logs_entity', 'audit_logs', ['entity_name', 'entity_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_user_id'), 'audit_logs', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_audit_logs_user_id'), table_name='audit_logs')
    op.drop_index('ix_audit_logs_entity', table_name='audit_logs')
    op.drop_table('audit_logs')

    _drop_audit_columns('receivers', include_created_at=False)
    for table in (
        'volantes',
        'titles',
        'positions',
        'organizations',
        'job_roles',
        'contacts',
        'addresses',
    ):
        _drop_audit_columns(table, include_created_at=True)
