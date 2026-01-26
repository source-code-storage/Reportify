"""Simple password reset using direct imports"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from passlib.context import CryptContext

# Create password hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
new_password = "password123"
hashed = pwd_context.hash(new_password)

print(f"Hashed password: {hashed}")
print(f"\nNow updating database...")

import sqlite3

conn = sqlite3.connect("report_assistant.db")
cursor = conn.cursor()

email = "mustaphaliaichi@gmail.com"

# Update the password
cursor.execute("UPDATE users SET hashed_password = ? WHERE email = ?", (hashed, email))
conn.commit()

# Verify the update
cursor.execute("SELECT email, name FROM users WHERE email = ?", (email,))
result = cursor.fetchone()

if result:
    print(f"✓ Password updated successfully!")
    print(f"  Email: {result[0]}")
    print(f"  Name: {result[1]}")
    print(f"  New password: {new_password}")
else:
    print(f"✗ User not found: {email}")

conn.close()
