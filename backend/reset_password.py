"""Reset user password"""

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()
try:
    email = "mustaphaliaichi@gmail.com"
    new_password = "password123"  # Change this to your desired password

    user = db.query(User).filter(User.email == email).first()

    if user:
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        print(f"✓ Password reset successfully for: {user.email}")
        print(f"  New password: {new_password}")
        print(f"\nYou can now login with:")
        print(f"  Email: {email}")
        print(f"  Password: {new_password}")
    else:
        print(f"✗ No user found with email: {email}")

finally:
    db.close()
