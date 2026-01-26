import sqlite3
import os

# Check both possible locations
db_paths = ["backend/report_assistant.db", "report_assistant.db"]

for db_path in db_paths:
    if os.path.exists(db_path):
        print(f"\n✅ Found database: {db_path}")
        print(f"   Size: {os.path.getsize(db_path) / 1024:.2f} KB")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        print(f"\n📊 Tables in database:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   - {table_name}: {count} rows")

        conn.close()
    else:
        print(f"❌ Not found: {db_path}")
