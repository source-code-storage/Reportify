"""
Initialize database directly without alembic
Using psycopg3 which handles encoding better
"""

from sqlalchemy import create_engine
from app.core.database import Base
from app.models import User

# Create engine with psycopg3
DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/report_assistant"
engine = create_engine(DATABASE_URL, echo=True)

print("Creating all tables...")
try:
    Base.metadata.create_all(bind=engine)
    print("\n✓ All tables created successfully!")

    # Verify tables were created
    from sqlalchemy import inspect

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"✓ Tables in database: {tables}")

except Exception as e:
    print(f"\n✗ Error creating tables: {e}")
    import traceback

    traceback.print_exc()
