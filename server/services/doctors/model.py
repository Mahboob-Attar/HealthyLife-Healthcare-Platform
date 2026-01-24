from db import get_connection


class DoctorModel:

    @staticmethod
    def find_by_email(email: str):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT id FROM doctors WHERE email=%s LIMIT 1", (email,))
        result = cur.fetchone()

        cur.close()
        conn.close()
        return result

    @staticmethod
    def find_by_phone(phone: str):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT id FROM doctors WHERE phone=%s LIMIT 1", (phone,))
        result = cur.fetchone()

        cur.close()
        conn.close()
        return result

    @staticmethod
    def create(data: dict):
        conn = get_connection()
        cur = conn.cursor()

        sql = """
            INSERT INTO doctors
            (name, phone, email, experience, specialization, services, clinic, location, photo_path, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cur.execute(sql, (
            data["name"],
            data["phone"],
            data["email"],
            data.get("experience"),
            data["specialization"],
            data.get("services"),
            data.get("clinic"),
            data.get("location"),
            data["photo_path"],
            data["created_at"]
        ))

        conn.commit()
        cur.close()
        conn.close()
        return True

    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT id, name, specialization, photo_path, clinic, location
            FROM doctors ORDER BY created_at DESC
        """)

        rows = cur.fetchall()

        cur.close()
        conn.close()
        return rows
