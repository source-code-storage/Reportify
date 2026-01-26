"""Test password reset via direct database access"""

import sqlite3
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# New password
new_password = "password123"
email = "mustaphaliaichi@gmail.com"

# Hash the password
hashed_password = pwd_context.hash(new_password)

# Connect to database
conn = sqlite3.connect("report_assistant.db")
cursor = conn.cursor()

try:
    # Check if user exists
    cursor.execute("SELECT id, email, name FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user:
        print(f"Found user: {user[1]} (ID: {user[0]}, Name: {user[2]})")

        # Update password
        cursor.execute(
            "UPDATE users SET password_hash = ? WHERE email = ?",
            (hashed_password, email),
        )
        conn.commit()

        print(f"\n✓ Password reset successful!")
        print(f"  Email: {email}")
        print(f"  Password: {new_password}")
        print(f"\nYou can now login at: http://localhost:5174/login")
    else:
        print(f"✗ User not found: {email}")

        # Show all users
        cursor.execute("SELECT email, name FROM users")
        all_users = cursor.fetchall()
        print(f"\nUsers in database ({len(all_users)}):")
        for u in all_users:
            print(f"  - {u[0]} ({u[1]})")

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
finally:
    conn.close()
