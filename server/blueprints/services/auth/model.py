from server.config.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel:

    @staticmethod
    def create_user(name, email, password, role):
        """Create user with hashed password."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            hashed = generate_password_hash(password)
            cur.execute("""
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, %s)
            """, (name, email, hashed, role))
            conn.commit()
            return True
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_user_by_email(email):
        """Fetch full user object"""
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT * FROM users WHERE email=%s", (email,))
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def user_exists(email):
        """Check if user exists by email"""
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM users WHERE email=%s", (email,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def update_password(email, new_password):
        """Reset / Update password"""
        conn = get_connection()
        cur = conn.cursor()
        try:
            hashed = generate_password_hash(new_password)
            cur.execute("UPDATE users SET password=%s WHERE email=%s", (hashed, email))
            conn.commit()
            return True
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def verify_password(hashed, plain):
        """Check plain text vs hashed"""
        return check_password_hash(hashed, plain)
