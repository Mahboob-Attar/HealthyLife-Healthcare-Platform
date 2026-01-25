from server.config.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel:

    @staticmethod
    def create_user(name, email, password, role):
        conn = get_connection()
        cur = conn.cursor()

        hashed = generate_password_hash(password)

        cur.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
        """, (name, email, hashed, role))

        conn.commit()
        cur.close()
        conn.close()
        return True

    @staticmethod
    def get_user_by_email(email):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        row = cur.fetchone()

        cur.close()
        conn.close()
        return row

    @staticmethod
    def verify_password(hashed, plain):
        return check_password_hash(hashed, plain)
