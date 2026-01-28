from flask import Flask
from dotenv import load_dotenv
import os

from server.config.db import get_connection
from server.session.mysql_session import MySQLSessionInterface

load_dotenv()

def create_app():
    app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static"
    )
    app.config["SESSION_COOKIE_NAME"] = "health_session"

    # Attach MySQL session interface
    app.session_interface = MySQLSessionInterface(
        db_conn_func=get_connection,
        table="sessions"
    )

    from server.blueprints import init_blueprints
    init_blueprints(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
