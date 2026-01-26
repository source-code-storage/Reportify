"""add_upload_job_model

Revision ID: 2d990085fb08
Revises: 001
Create Date: 2026-01-11 13:48:05.219799+00:00

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2d990085fb08"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "upload_jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("report_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("file_type", sa.String(length=50), nullable=False),
        sa.Column("file_format", sa.String(length=50), nullable=False),
        sa.Column("file_size", sa.Integer(), nullable=False),
        sa.Column("file_path", sa.String(length=500), nullable=True),
        sa.Column(
            "status", sa.String(length=50), nullable=False, server_default="pending"
        ),
        sa.Column("progress", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("celery_task_id", sa.String(length=255), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("processing_details", sa.Text(), nullable=True),
        sa.Column("note_id", sa.Integer(), nullable=True),
        sa.Column("template_structure_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["report_id"], ["reports.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["note_id"], ["notes.id"], ondelete="SET NULL"),
    )
    op.create_index(op.f("ix_upload_jobs_id"), "upload_jobs", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_upload_jobs_id"), table_name="upload_jobs")
    op.drop_table("upload_jobs")
