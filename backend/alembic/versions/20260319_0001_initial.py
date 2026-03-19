"""initial schema

Revision ID: 20260319_0001
Revises:
Create Date: 2026-03-19 17:30:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260319_0001"
down_revision = None
branch_labels = None
depends_on = None


user_role = postgresql.ENUM("admin", "editor", "viewer", "client", name="userrole", create_type=False)
inquiry_status = postgresql.ENUM("new", "qualified", "proposal", "booked", "closed", name="inquirystatus", create_type=False)


def upgrade() -> None:
    bind = op.get_bind()
    user_role.create(bind, checkfirst=True)
    inquiry_status.create(bind, checkfirst=True)

    op.create_table(
        "artists",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("headline", sa.String(length=255), nullable=False),
        sa.Column("discipline", sa.String(length=100), nullable=False),
        sa.Column("group_size", sa.String(length=50), nullable=False),
        sa.Column("mood", sa.String(length=100), nullable=False),
        sa.Column("venue_type", sa.String(length=100), nullable=False),
        sa.Column("technical_requirements", sa.JSON(), nullable=False),
        sa.Column("bio", sa.Text(), nullable=False),
        sa.Column("featured", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_new", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("location", sa.String(length=150), nullable=False, server_default="London"),
        sa.Column("travel_ready", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("hero_video_url", sa.String(length=500), nullable=True),
        sa.Column("teaser_video_url", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_artists_name"), "artists", ["name"], unique=False)
    op.create_index(op.f("ix_artists_slug"), "artists", ["slug"], unique=False)
    op.create_index(op.f("ix_artists_discipline"), "artists", ["discipline"], unique=False)
    op.create_index(op.f("ix_artists_group_size"), "artists", ["group_size"], unique=False)
    op.create_index(op.f("ix_artists_mood"), "artists", ["mood"], unique=False)
    op.create_index(op.f("ix_artists_venue_type"), "artists", ["venue_type"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False, server_default="viewer"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "service_pages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_service_pages_slug"), "service_pages", ["slug"], unique=False)

    op.create_table(
        "inquiries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_name", sa.String(length=200), nullable=False),
        sa.Column("contact_name", sa.String(length=200), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("event_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("location", sa.String(length=200), nullable=False),
        sa.Column("venue_type", sa.String(length=100), nullable=True),
        sa.Column("ceiling_height_meters", sa.Integer(), nullable=True),
        sa.Column("budget_min", sa.Numeric(10, 2), nullable=True),
        sa.Column("budget_max", sa.Numeric(10, 2), nullable=True),
        sa.Column("preferred_disciplines", sa.JSON(), nullable=False),
        sa.Column("preferred_artist_slugs", sa.JSON(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("lead_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("source", sa.String(length=100), nullable=False, server_default="website"),
        sa.Column("status", inquiry_status, nullable=False, server_default="new"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index(op.f("ix_inquiries_email"), "inquiries", ["email"], unique=False)
    op.create_index(op.f("ix_inquiries_event_type"), "inquiries", ["event_type"], unique=False)

    op.create_table(
        "media_assets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("artist_id", sa.Integer(), sa.ForeignKey("artists.id", ondelete="CASCADE"), nullable=True),
        sa.Column("asset_type", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.Column("thumbnail_url", sa.String(length=500), nullable=True),
        sa.Column("alt_text", sa.String(length=255), nullable=True),
        sa.Column("asset_metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "testimonials",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("artist_id", sa.Integer(), sa.ForeignKey("artists.id", ondelete="SET NULL"), nullable=True),
        sa.Column("client_name", sa.String(length=200), nullable=False),
        sa.Column("client_type", sa.String(length=100), nullable=False),
        sa.Column("quote", sa.Text(), nullable=False),
        sa.Column("event_name", sa.String(length=200), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("inquiry_id", sa.Integer(), sa.ForeignKey("inquiries.id", ondelete="SET NULL"), nullable=True),
        sa.Column("artist_id", sa.Integer(), sa.ForeignKey("artists.id", ondelete="SET NULL"), nullable=True),
        sa.Column("booking_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=100), nullable=False, server_default="tentative"),
        sa.Column("fee_amount", sa.Numeric(10, 2), nullable=True),
        sa.Column("deposit_paid", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("contract_url", sa.String(length=500), nullable=True),
        sa.Column("production_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "availability_slots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("artist_id", sa.Integer(), sa.ForeignKey("artists.id", ondelete="CASCADE"), nullable=False),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="available"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index(op.f("ix_availability_slots_artist_id"), "availability_slots", ["artist_id"], unique=False)

    op.create_table(
        "case_studies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("event_context", sa.String(length=150), nullable=False),
        sa.Column("challenge", sa.Text(), nullable=False),
        sa.Column("solution", sa.Text(), nullable=False),
        sa.Column("client_name", sa.String(length=200), nullable=True),
        sa.Column("hero_image_url", sa.String(length=500), nullable=True),
        sa.Column("video_url", sa.String(length=500), nullable=True),
        sa.Column("featured_artist_slugs", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_case_studies_slug"), "case_studies", ["slug"], unique=False)

    op.create_table(
        "audit_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_email", sa.String(length=255), nullable=True),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.String(length=100), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    op.drop_table("audit_events")
    op.drop_index(op.f("ix_case_studies_slug"), table_name="case_studies")
    op.drop_table("case_studies")
    op.drop_index(op.f("ix_availability_slots_artist_id"), table_name="availability_slots")
    op.drop_table("availability_slots")
    op.drop_table("bookings")
    op.drop_table("testimonials")
    op.drop_table("media_assets")
    op.drop_index(op.f("ix_inquiries_event_type"), table_name="inquiries")
    op.drop_index(op.f("ix_inquiries_email"), table_name="inquiries")
    op.drop_table("inquiries")
    op.drop_index(op.f("ix_service_pages_slug"), table_name="service_pages")
    op.drop_table("service_pages")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_artists_venue_type"), table_name="artists")
    op.drop_index(op.f("ix_artists_mood"), table_name="artists")
    op.drop_index(op.f("ix_artists_group_size"), table_name="artists")
    op.drop_index(op.f("ix_artists_discipline"), table_name="artists")
    op.drop_index(op.f("ix_artists_slug"), table_name="artists")
    op.drop_index(op.f("ix_artists_name"), table_name="artists")
    op.drop_table("artists")

    bind = op.get_bind()
    inquiry_status.drop(bind, checkfirst=True)
    user_role.drop(bind, checkfirst=True)