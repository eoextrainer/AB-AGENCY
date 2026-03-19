"""artist user profiles

Revision ID: 20260319_0002
Revises: 20260319_0001
Create Date: 2026-03-19 18:10:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260319_0002"
down_revision = "20260319_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("artists", sa.Column("years_experience", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("artists", sa.Column("portrait_image_url", sa.String(length=500), nullable=True))
    op.add_column("artists", sa.Column("spoken_languages", sa.JSON(), nullable=False, server_default=sa.text("'[]'")))
    op.add_column("artists", sa.Column("performance_resume", sa.JSON(), nullable=False, server_default=sa.text("'[]'")))

    op.add_column("users", sa.Column("username", sa.String(length=100), nullable=True))
    op.add_column("users", sa.Column("artist_id", sa.Integer(), nullable=True))
    op.create_foreign_key("fk_users_artist_id", "users", "artists", ["artist_id"], ["id"], ondelete="SET NULL")

    op.execute("UPDATE users SET username = 'admin' WHERE email = 'admin@ab-agency.com'")
    op.execute("UPDATE users SET username = split_part(email, '@', 1) WHERE username IS NULL")

    op.alter_column("users", "username", nullable=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_unique_constraint("uq_users_artist_id", "users", ["artist_id"])


def downgrade() -> None:
    op.drop_constraint("uq_users_artist_id", "users", type_="unique")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_constraint("fk_users_artist_id", "users", type_="foreignkey")
    op.drop_column("users", "artist_id")
    op.drop_column("users", "username")

    op.drop_column("artists", "performance_resume")
    op.drop_column("artists", "spoken_languages")
    op.drop_column("artists", "portrait_image_url")
    op.drop_column("artists", "years_experience")