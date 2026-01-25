from flask import jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from server.config.db import get_connection

# ==========================
# SIGNUP
# ==========================
def auth_signup(data):
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not name or not email or not password or not role:
        return jsonify({"status": "error", "msg": "All fields required"}), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Check if user exists
    cur.execute("SELECT id FROM users WHERE email=%s", (email,))
    if cur.fetchone():
        return jsonify({"status": "error", "msg": "Email already registered"}), 400

    hashed_pass = generate_password_hash(password)

    cur.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (%s, %s, %s, %s)
    """, (name, email, hashed_pass, role))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "success", "msg": "Account created"}), 200


# ==========================
# LOGIN
# ==========================
def auth_login(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "error", "msg": "Email & password required"}), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()

    if not user:
        return jsonify({"status": "error", "msg": "User not found"}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({"status": "error", "msg": "Incorrect password"}), 400

    # SET SESSION
    session["logged_in"] = True
    session["user_id"] = user["id"]
    session["role"] = user["role"]

    return jsonify({
        "status": "success",
        "msg": "Login successful",
        "role": user["role"]
    }), 200


# ==========================
# RESET PASSWORD
# ==========================
def reset_password(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "error", "msg": "Email & new password required"}), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    hashed_pass = generate_password_hash(password)

    cur.execute("UPDATE users SET password=%s WHERE email=%s", (hashed_pass, email))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"status": "success", "msg": "Password reset complete"}), 200
