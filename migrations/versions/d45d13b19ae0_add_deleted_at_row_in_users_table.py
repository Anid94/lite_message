"""Add deleted_at row in users table

Revision ID: d45d13b19ae0
Revises: af53620dd7a7
Create Date: 2026-11-20 13:53:22.285798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd45d13b19ae0'
down_revision: Union[str, Sequence[str], None] = 'af53620dd7a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sender_id", sa.Integer(), nullable=False),
        sa.Column("recipient_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["recipient_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sender_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_sender_recipient_messages",
        "messages",
        ["sender_id", "recipient_id", "created_at"],
        unique=False,
    )

    op.add_column(
        "users",
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "deleted_at")

    op.drop_index(
        "ix_sender_recipient_messages",
        table_name="messages",
    )

    op.drop_table("messages")