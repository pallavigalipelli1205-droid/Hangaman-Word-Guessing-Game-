
import bcrypt

from database import get_connection


# Register a new user
def register_user(username, email, password):

    if not username.strip() or not email.strip():
        return False, "Username and email are required."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users
            (username, email, password_hash)
            VALUES (?, ?, ?)
        """, (username.strip(), email.strip(), password_hash))

        conn.commit()

        return True, "Registration successful!"

    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return False, "Username or email already exists."

        return False, "Registration failed."

    finally:
        conn.close()


# Login existing user
def login_user(username, password):

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_id, username, password_hash
            FROM users
            WHERE username = ?
        """, (username.strip(),))

        user = cursor.fetchone()

        if user is None:
            return None

        stored_hash = user[2].encode("utf-8")

        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_hash
        ):
            return {
                "user_id": user[0],
                "username": user[1]
            }

        return None

    finally:
        conn.close()
