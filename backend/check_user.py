"""Quick script to check if a user exists"""

from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()
try:
    email = "mustaphaliaichi@gmail.com"
    user = db.query(User).filter(User.email == email).first()

    if user:
        print(f"✓ User found: {user.email} (ID: {user.id})")
        print(f"  Name: {user.name}")
        print(f"  Active: {user.is_active}")
        print(f"  Created: {user.created_at}")
    else:
        print(f"✗ No user found with email: {email}")
        print("\nYou need to register first!")
        print("Use the registration endpoint or create a user manually.")

    # Show all users
    all_users = db.query(User).all()
    print(f"\nTotal users in database: {len(all_users)}")
    for u in all_users:
        print(f"  - {u.email} ({u.name})")

finally:
    db.close()
