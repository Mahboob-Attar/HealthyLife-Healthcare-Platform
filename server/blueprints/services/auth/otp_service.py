from datetime import datetime, timedelta
import random
from server.config.db import get_connection
from server.config.email import send_email


def generate_otp():
    return str(random.randint(100000, 999999))


# Create & store OTP
def create_and_send_otp(email, purpose="signup"):
    try:
        otp = generate_otp()
        expires = datetime.now() + timedelta(minutes=2)

        conn = get_connection()
        cur = conn.cursor()

        # Clean old OTPs
        cur.execute("DELETE FROM otp_verification WHERE expires_at < NOW() OR used = 1")

        # Insert new OTP
        cur.execute("""
            INSERT INTO otp_verification (email, otp, purpose, expires_at, used)
            VALUES (%s, %s, %s, %s, 0)
        """, (email, otp, purpose, expires))

        conn.commit()
        cur.close()
        conn.close()

        # Send email
        send_email(email, "HealthyLife OTP", f"Your OTP is: {otp}")

        return {"status": "success", "msg": "OTP sent"}

    except Exception as e:
        return {"status": "error", "msg": f"Failed to send OTP: {str(e)}"}


# Validate OTP
def verify_otp(email, otp, purpose="signup"):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Remove expired
    cur.execute("DELETE FROM otp_verification WHERE expires_at < NOW()")

    # Check OTP
    cur.execute("""
        SELECT * FROM otp_verification
        WHERE email=%s AND otp=%s AND purpose=%s AND used=0
        ORDER BY id DESC LIMIT 1
    """, (email, otp, purpose))

    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return {"status": "error", "msg": "Invalid or expired OTP"}

    # Mark used
    cur.execute("UPDATE otp_verification SET used=1 WHERE id=%s", (row['id'],))
    conn.commit()

    cur.close()
    conn.close()

    return {"status": "success", "msg": "OTP verified"}
