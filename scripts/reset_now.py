"""
Reset the database immediately - No confirmation needed
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from sqlalchemy import create_engine, text
from app.core.config import settings


def reset_database():
    """Delete all data from the database"""

    print("🗑️  Resetting database...")
    print(f"📍 Database: {settings.DATABASE_URL}")

    # Create engine
    engine = create_engine(settings.DATABASE_URL)

    try:
        with engine.connect() as conn:
            # Start transaction
            trans = conn.begin()

            try:
                # Delete in correct order (respecting foreign keys)
                print("\n🔄 Deleting data...")

                # Delete note chunks first (has foreign key to notes)
                try:
                    result = conn.execute(text("DELETE FROM note_chunks"))
                    print(f"   ✅ Deleted {result.rowcount} note chunks")
                except Exception as e:
                    print(f"   ⚠️  Note chunks: {e}")

                # Delete notes (has foreign key to reports)
                try:
                    result = conn.execute(text("DELETE FROM notes"))
                    print(f"   ✅ Deleted {result.rowcount} notes")
                except Exception as e:
                    print(f"   ⚠️  Notes: {e}")

                # Delete template sections (has foreign key to reports)
                try:
                    result = conn.execute(text("DELETE FROM template_sections"))
                    print(f"   ✅ Deleted {result.rowcount} template sections")
                except Exception as e:
                    print(f"   ⚠️  Template sections: {e}")

                # Delete report sections (has foreign key to reports)
                try:
                    result = conn.execute(text("DELETE FROM report_sections"))
                    print(f"   ✅ Deleted {result.rowcount} report sections")
                except Exception as e:
                    print(f"   ⚠️  Report sections: {e}")

                # Delete reports (has foreign key to users)
                try:
                    result = conn.execute(text("DELETE FROM reports"))
                    print(f"   ✅ Deleted {result.rowcount} reports")
                except Exception as e:
                    print(f"   ⚠️  Reports: {e}")

                # Commit transaction
                trans.commit()

                print("\n✅ Database reset successfully!")
                print(
                    "\n📝 Note: Users were NOT deleted. You can still login with existing accounts."
                )

            except Exception as e:
                trans.rollback()
                print(f"\n❌ Error during reset: {e}")
                raise

    except Exception as e:
        print(f"\n❌ Failed to connect to database: {e}")
        return False

    finally:
        engine.dispose()

    return True


def reset_qdrant():
    """Reset Qdrant vector database"""
    try:
        from qdrant_client import QdrantClient

        print("\n🔄 Resetting Qdrant vector database...")

        client = QdrantClient(url=settings.QDRANT_URL)

        # Delete the collection if it exists
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

    except ImportError:
        print("   ⚠️  Qdrant client not available, skipping...")
    except Exception as e:
        print(f"   ⚠️  Could not connect to Qdrant: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE RESET - STARTING NOW")
    print("=" * 60)
    print()

    success = reset_database()

    if success:
        reset_qdrant()

        print("\n" + "=" * 60)
        print("✅ RESET COMPLETE!")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Login with your existing account")
        print("2. Create new reports")
        print("3. Upload the new template: PFE_Project_Template.pdf")
        print("\n🚀 Ready for fresh testing!")
    else:
        print("\n❌ Reset failed. Please check the errors above.")
