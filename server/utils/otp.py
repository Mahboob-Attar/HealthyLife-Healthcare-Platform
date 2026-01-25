import random
from datetime import datetime, timedelta
from server.config.db import get_connection
from server.config.email import send_email


def generate_otp():
    """Generate a 6-digit random OTP"""
    return str(random.randint(100000, 999999))


def store_otp_and_send_email(email, purpose="signup"):
    otp = generate_otp()
    expires = datetime.now() + timedelta(minutes=2)  # OTP valid for 2 minutes

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Delete expired or used OTPs for safety
        cur.execute("DELETE FROM otp_verification WHERE expires_at < NOW() OR used = 1")

        # Insert fresh OTP
        cur.execute("""
            INSERT INTO otp_verification (email, otp, purpose, expires_at, used)
            VALUES (%s, %s, %s, %s, 0)
        """, (email, otp, purpose, expires))

        conn.commit()
        cur.close()
        conn.close()

        # Updated Email Message
        message = (
            f"Hello,\n\n"
            f"Your HealthyLife OTP is: {otp}\n\n"
            f"⏳ Validity: 2 minutes\n"
            f"⚠️ Action: Please complete the signup as early as possible before OTP expires.\n\n"
            f"If you did not request this OTP, please ignore this email.\n\n"
            f"Regards,\n"
            f"HealthyLife Team"
        )

        send_email(email, "HealthyLife Verification OTP", message)

        return True, "OTP sent successfully"

    except Exception as e:
        print("OTP Error:", e)
        return False, "Failed to send OTP"
