"""Initiales ImmoFix-Schema mit Admin-Benutzern.

Revision ID: 0001
Revises:
Create Date: 2026-08-06
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=180), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "properties",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("address", sa.String(length=200), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("postal_code", sa.String(length=20)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "contractors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("company", sa.String(length=120)),
        sa.Column("phone", sa.String(length=50)),
        sa.Column("email", sa.String(length=120)),
        sa.Column("specialization", sa.String(length=100), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "apartments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("property_id", sa.Integer(), sa.ForeignKey("properties.id", ondelete="CASCADE"), nullable=False),
        sa.Column("apartment_number", sa.String(length=30), nullable=False),
        sa.Column("floor", sa.String(length=30)),
        sa.Column("contact_name", sa.String(length=120)),
        sa.Column("contact_phone", sa.String(length=50)),
        sa.Column("contact_email", sa.String(length=120)),
        sa.Column("notes", sa.Text()),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_apartments_property_id", "apartments", ["property_id"])
    op.create_index("ix_apartments_property_number", "apartments", ["property_id", "apartment_number"], unique=True)

    op.create_table(
        "tickets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("apartment_id", sa.Integer(), sa.ForeignKey("apartments.id"), nullable=False),
        sa.Column("contractor_id", sa.Integer(), sa.ForeignKey("contractors.id")),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("priority", sa.String(length=20), nullable=False, server_default="normal"),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="new"),
        sa.Column("reported_by", sa.String(length=120), nullable=False),
        sa.Column("reporter_phone", sa.String(length=50)),
        sa.Column("reporter_email", sa.String(length=120)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_tickets_apartment_id", "tickets", ["apartment_id"])
    op.create_index("ix_tickets_contractor_id", "tickets", ["contractor_id"])
    op.create_index("ix_tickets_status_priority", "tickets", ["status", "priority"])
    op.create_index("ix_tickets_created_at", "tickets", ["created_at"])


def downgrade() -> None:
    op.drop_table("tickets")
    op.drop_table("apartments")
    op.drop_table("contractors")
    op.drop_table("properties")
    op.drop_table("users")
