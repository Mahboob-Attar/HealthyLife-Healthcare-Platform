from datetime import datetime
from flask import jsonify
from server.config.db import get_connection

def verify_otp(email, otp, purpose="signup"):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Remove expired OTPs first
    cur.execute("DELETE FROM otp_verification WHERE expires_at < NOW()")

    # Check OTP
    cur.execute("""
        SELECT * FROM otp_verification 
        WHERE email=%s AND otp=%s AND purpose=%s AND used=0
        ORDER BY id DESC LIMIT 1
    """, (email, otp, purpose))

    row = cur.fetchone()

    if not row:
        return jsonify({"status": "error", "msg": "Invalid or expired OTP"}), 400

    # Mark as used
    cur.execute("UPDATE otp_verification SET used=1 WHERE id=%s", (row['id'],))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "success", "msg": "OTP verified"})
