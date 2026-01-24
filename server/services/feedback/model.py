from db import get_connection

class FeedbackModel:

    @staticmethod
    def create(data: dict):
        conn = get_connection()
        cur = conn.cursor()

        sql = """
            INSERT INTO feedback (username, rating, review, created_at)
            VALUES (%s, %s, %s, %s)
        """

        cur.execute(sql, (
            data["username"],
            data["rating"],
            data["review"],
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

        cur.execute("SELECT * FROM feedback ORDER BY created_at DESC")
        rows = cur.fetchall()

        cur.close()
        conn.close()
        return rows
