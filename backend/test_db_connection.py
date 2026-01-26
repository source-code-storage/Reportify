"""
Test database connection
"""

import psycopg2
import os

# Set encoding to UTF-8
os.environ["PGCLIENTENCODING"] = "UTF8"

try:
    # Try to connect to PostgreSQL with explicit encoding
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="report_assistant",
        user="postgres",
        password="postgres",
        client_encoding="UTF8",
    )

    print("✓ Database connection successful!")

    # Test creating the users table
    cursor = conn.cursor()

    # Check if database exists
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✓ PostgreSQL version: {version[0]}")

    # Check if users table exists
    cursor.execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'users'
        );
    """
    )
    table_exists = cursor.fetchone()[0]

    if table_exists:
        print("✓ Users table already exists")
    else:
        print("ℹ Users table does not exist yet (will be created by alembic)")

    cursor.close()
    conn.close()

    print("\n✓ All database checks passed!")

except Exception as e:
    print(f"✗ Database connection failed: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback

    traceback.print_exc()
    print("\nMake sure Docker PostgreSQL is running:")
    print("  docker-compose up -d")
