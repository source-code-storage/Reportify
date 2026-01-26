"""create_notes_tables

Revision ID: 515d52c1b4d4
Revises: 005
Create Date: 2026-01-18 16:24:40.986370+00:00

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "515d52c1b4d4"
down_revision = "005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create notes table
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("report_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("file_type", sa.String(length=50), nullable=False),
        sa.Column("file_size", sa.Integer(), nullable=False),
        sa.Column("file_path", sa.String(length=500), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("processing_error", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["report_id"], ["reports.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_notes_id"), "notes", ["id"], unique=False)

    # Create note_embeddings table
    op.create_table(
        "note_embeddings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("note_id", sa.Integer(), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("chunk_text", sa.Text(), nullable=False),
        sa.Column("embedding_vector", sa.Text(), nullable=True),
        sa.Column("qdrant_id", sa.String(length=100), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["note_id"], ["notes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_note_embeddings_id"), "note_embeddings", ["id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_note_embeddings_id"), table_name="note_embeddings")
    op.drop_table("note_embeddings")
    op.drop_index(op.f("ix_notes_id"), table_name="notes")
    op.drop_table("notes")
