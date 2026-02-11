import uuid
import json
from datetime import datetime, timedelta
from flask.sessions import SessionInterface, SessionMixin


class MySQLSession(dict, SessionMixin):
    def __init__(self, initial=None, session_id=None):
        super().__init__(initial or {})
        self.session_id = session_id


class MySQLSessionInterface(SessionInterface):
    def __init__(self, db_conn_func, table="sessions", lifetime_minutes=15):
        self.db_conn_func = db_conn_func
        self.table = table
        self.lifetime_minutes = lifetime_minutes

    # OPEN SESSION
    def open_session(self, app, request):
        cookie_name = app.config.get("SESSION_COOKIE_NAME", "session")
        session_id = request.cookies.get(cookie_name)

        if not session_id:
            return MySQLSession(session_id=str(uuid.uuid4()))

        with self.db_conn_func() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(
                    f"SELECT data, expiry FROM {self.table} WHERE session_id=%s",
                    (session_id,)
                )
                row = cur.fetchone()

                if row:
                    # Check expiry
                    if row["expiry"] and row["expiry"] > datetime.utcnow():
                        data = json.loads(row["data"])
                        return MySQLSession(data, session_id=session_id)
                    else:
                        # Expired → delete
                        cur.execute(
                            f"DELETE FROM {self.table} WHERE session_id=%s",
                            (session_id,)
                        )
                        conn.commit()

        # Create new session if expired or not found
        return MySQLSession(session_id=str(uuid.uuid4()))

    # SAVE SESSION
    def save_session(self, app, session, response):
        cookie_name = app.config.get("SESSION_COOKIE_NAME", "session")

        # If session is empty → delete it
        if not session:
            response.delete_cookie(cookie_name)
            return

        session_id = session.session_id
        expiry = datetime.utcnow() + timedelta(minutes=self.lifetime_minutes)
        data = json.dumps(dict(session))

        with self.db_conn_func() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    REPLACE INTO {self.table} 
                    (session_id, data, expiry) 
                    VALUES (%s, %s, %s)
                    """,
                    (session_id, data, expiry)
                )
                conn.commit()

        response.set_cookie(
            cookie_name,
            session_id,
            httponly=True,
            secure=True,       
            samesite="Lax"
        )
