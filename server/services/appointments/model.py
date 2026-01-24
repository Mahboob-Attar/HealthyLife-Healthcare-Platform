from db import get_connection

class AppointmentModel:

    @staticmethod
    def get_all_cities():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT DISTINCT location FROM doctors ORDER BY location ASC")
        rows = [row["location"] for row in cur.fetchall()]

        cur.close()
        conn.close()
        return rows

    @staticmethod
    def get_all_doctors():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM doctors ORDER BY created_at DESC")
        rows = cur.fetchall()

        cur.close()
        conn.close()
        return rows

    @staticmethod
    def get_doctors_by_city(city):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute(
            "SELECT * FROM doctors WHERE location=%s ORDER BY created_at DESC",
            (city,)
        )
        rows = cur.fetchall()

        cur.close()
        conn.close()
        return rows
