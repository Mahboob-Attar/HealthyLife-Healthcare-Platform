from flask import jsonify, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from server.config.db import get_connection
from server.config.email import send_email_html
from datetime import datetime

def auth_signup(data):
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not name or not email or not password or not role:
        return jsonify({"status": "error", "msg": "All fields required"}), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

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

    # SEND ACCOUNT CREATED EMAIL
    html = render_template("emails/accountcreated_email.html",
                           user_name=name,
                           year=datetime.now().year)

    send_email_html(email, "Account Created Successfully", html)

    return jsonify({"status": "success", "msg": "Account created successfully"}), 200



def auth_login(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "error", "msg": "Email & password required"}), 400

    email = email.strip().lower()

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        return jsonify({"status": "error", "msg": "User not found"}), 404

    if not check_password_hash(user["password"], password):
        cur.close()
        conn.close()
        return jsonify({"status": "error", "msg": "Incorrect password"}), 400

    cur.close()
    conn.close()

    session["logged_in"] = True
    session["user_id"] = user["id"]
    session["role"] = user["role"]

    return jsonify({"status": "success", "msg": "Login successful", "role": user["role"]}), 200



def reset_password(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "error", "msg": "Email & new password required"}), 400

    email = email.strip().lower()

    if len(password) < 6:
        return jsonify({"status": "error", "msg": "Password must be at least 6 characters"}), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT id FROM users WHERE email=%s", (email,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"status": "error", "msg": "Email not found"}), 404

    hashed_pass = generate_password_hash(password)

    cur.execute("UPDATE users SET password=%s WHERE email=%s", (hashed_pass, email))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"status": "success", "msg": "Password reset complete"}), 200
