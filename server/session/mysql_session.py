import uuid
import json
from datetime import datetime, timedelta
from flask.sessions import SessionInterface, SessionMixin


class MySQLSession(dict, SessionMixin):
    def __init__(self, initial=None, session_id=None):
        super().__init__(initial or {})
        self.session_id = session_id


class MySQLSessionInterface(SessionInterface):
    def __init__(self, db_conn_func, table="sessions", lifetime_days=1):
        self.db_conn_func = db_conn_func
        self.table = table
        self.lifetime_days = lifetime_days

    def open_session(self, app, request):
        cookie_name = app.config.get("SESSION_COOKIE_NAME", "session")
        session_id = request.cookies.get(cookie_name)

        with self.db_conn_func() as conn:
            with conn.cursor(dictionary=True) as cur:
                if session_id:
                    cur.execute(
                        f"SELECT data FROM {self.table} WHERE session_id=%s",
                        (session_id,)
                    )
                    row = cur.fetchone()
                    if row:
                        data = json.loads(row["data"])
                        return MySQLSession(data, session_id=session_id)

        # Create new session if not found
        new_id = str(uuid.uuid4())
        return MySQLSession(session_id=new_id)

    def save_session(self, app, session, response):
        cookie_name = app.config.get("SESSION_COOKIE_NAME", "session")
        session_id = session.session_id
        expiry = datetime.utcnow() + timedelta(days=self.lifetime_days)
        data = json.dumps(dict(session))

        with self.db_conn_func() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"REPLACE INTO {self.table} (session_id, data, expiry) VALUES (%s, %s, %s)",
                    (session_id, data, expiry)
                )
                conn.commit()

        response.set_cookie(
            cookie_name,
            session_id,
            httponly=True,
            samesite="Lax",
            secure=False  # set True in HTTPS production
        )
