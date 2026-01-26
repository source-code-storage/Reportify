"""create template structure tables

Revision ID: 005
Revises: 2d990085fb08
Create Date: 2026-01-14

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = "005"
down_revision = "2d990085fb08"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create template_structures table
    op.create_table(
        "template_structures",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("report_id", sa.Integer(), nullable=False),
        sa.Column("upload_job_id", sa.Integer(), nullable=True),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("file_path", sa.String(length=500), nullable=False),
        sa.Column("total_pages", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("full_text", sa.Text(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column(
            "status", sa.String(length=50), nullable=False, server_default="pending"
        ),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("processed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["report_id"], ["reports.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["upload_job_id"], ["upload_jobs.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_template_structures_id"), "template_structures", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_template_structures_report_id"),
        "template_structures",
        ["report_id"],
        unique=False,
    )

    # Create template_sections table
    op.create_table(
        "template_sections",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("template_id", sa.Integer(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("level", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("page_number", sa.Integer(), nullable=True),
        sa.Column("position_top", sa.Float(), nullable=True),
        sa.Column("font_size", sa.Float(), nullable=True),
        sa.Column("font_name", sa.String(length=100), nullable=True),
        sa.Column("is_bold", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("word_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.ForeignKeyConstraint(
            ["template_id"], ["template_structures.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"], ["template_sections.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_template_sections_id"), "template_sections", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_template_sections_template_id"),
        "template_sections",
        ["template_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_template_sections_parent_id"),
        "template_sections",
        ["parent_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_template_sections_parent_id"), table_name="template_sections"
    )
    op.drop_index(
        op.f("ix_template_sections_template_id"), table_name="template_sections"
    )
    op.drop_index(op.f("ix_template_sections_id"), table_name="template_sections")
    op.drop_table("template_sections")

    op.drop_index(
        op.f("ix_template_structures_report_id"), table_name="template_structures"
    )
    op.drop_index(op.f("ix_template_structures_id"), table_name="template_structures")
    op.drop_table("template_structures")
