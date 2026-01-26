import sqlite3
import os

db_path = "backend/report_assistant.db"

print("=" * 60)
print("DELETE ALL REPORTS")
print("=" * 60)

if not os.path.exists(db_path):
    print(f"\n❌ Database not found: {db_path}")
    exit(1)

print(f"\n📍 Database: {db_path}")
print(f"   Size: {os.path.getsize(db_path) / 1024:.2f} KB")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Show current counts
print("\n📊 Current data:")
cursor.execute("SELECT COUNT(*) FROM reports")
reports_count = cursor.fetchone()[0]
print(f"   - Reports: {reports_count}")

cursor.execute("SELECT COUNT(*) FROM report_sections")
sections_count = cursor.fetchone()[0]
print(f"   - Report Sections: {sections_count}")

cursor.execute("SELECT COUNT(*) FROM notes")
notes_count = cursor.fetchone()[0]
print(f"   - Notes: {notes_count}")

cursor.execute("SELECT COUNT(*) FROM template_sections")
template_sections_count = cursor.fetchone()[0]
print(f"   - Template Sections: {template_sections_count}")

cursor.execute("SELECT COUNT(*) FROM template_structures")
template_structures_count = cursor.fetchone()[0]
print(f"   - Template Structures: {template_structures_count}")

cursor.execute("SELECT COUNT(*) FROM upload_jobs")
upload_jobs_count = cursor.fetchone()[0]
print(f"   - Upload Jobs: {upload_jobs_count}")

print("\n🗑️  Deleting all data...")

try:
    # Delete in correct order (respecting foreign keys)

    # Delete note embeddings first
    cursor.execute("DELETE FROM note_embeddings")
    print(f"   ✅ Deleted note embeddings")

    # Delete notes
    cursor.execute("DELETE FROM notes")
    print(f"   ✅ Deleted {notes_count} notes")

    # Delete template sections
    cursor.execute("DELETE FROM template_sections")
    print(f"   ✅ Deleted {template_sections_count} template sections")

    # Delete template structures
    cursor.execute("DELETE FROM template_structures")
    print(f"   ✅ Deleted {template_structures_count} template structures")

    # Delete report sections
    cursor.execute("DELETE FROM report_sections")
    print(f"   ✅ Deleted {sections_count} report sections")

    # Delete upload jobs
    cursor.execute("DELETE FROM upload_jobs")
    print(f"   ✅ Deleted {upload_jobs_count} upload jobs")

    # Delete reports
    cursor.execute("DELETE FROM reports")
    print(f"   ✅ Deleted {reports_count} reports")

    # Commit changes
    conn.commit()

    print("\n✅ All reports and related data deleted successfully!")
    print("\n📝 Note: Users were NOT deleted. You can still login.")

    # Show new counts
    print("\n📊 After deletion:")
    cursor.execute("SELECT COUNT(*) FROM reports")
    print(f"   - Reports: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM report_sections")
    print(f"   - Report Sections: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM notes")
    print(f"   - Notes: {cursor.fetchone()[0]}")

except Exception as e:
    conn.rollback()
    print(f"\n❌ Error: {e}")
finally:
    conn.close()

# Also reset Qdrant
print("\n🔄 Resetting Qdrant vector database...")
try:
    from qdrant_client import QdrantClient

    client = QdrantClient(url="http://localhost:6333")

    try:
        collections = client.get_collections().collections
        collection_names = [c.name for c in collections]

        if "notes" in collection_names:
            client.delete_collection("notes")
            print("   ✅ Deleted 'notes' collection from Qdrant")
        else:
            print("   ℹ️  No 'notes' collection found in Qdrant")
    except Exception as e:
        print(f"   ⚠️  Could not reset Qdrant: {e}")

except Exception as e:
    print(f"   ⚠️  Qdrant not available: {e}")

print("\n" + "=" * 60)
print("✅ RESET COMPLETE!")
print("=" * 60)
print("\n🚀 You can now:")
print("   1. Refresh your browser")
print("   2. Create new reports")
print("   3. Upload the template: PFE_Project_Template.pdf")
print("\n✨ Ready for fresh testing!")
