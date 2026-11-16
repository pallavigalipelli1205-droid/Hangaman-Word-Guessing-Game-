
from database import create_tables

create_tables()
from auth import register_user, login_user

# Register user
success, message = register_user(
    "pallavi_test",
    "pallavi_test@example.com",
    "Python@123"
)

print("Registration:", message)

# Login user
user = login_user("pallavi_test ", "Python@123")

if user:
    print("Login successful!")
    print("Welcome:", user["username"])
else:
    print("Invalid username or password.")

# Test wrong password
wrong_user = login_user("pallavi_test", "Wrong@123")

if wrong_user is None:
    print("Wrong password rejected successfully!")
