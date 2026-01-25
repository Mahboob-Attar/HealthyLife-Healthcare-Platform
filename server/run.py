from flask import Flask
from flask_session import Session
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static"
    )

    # SECRET KEY for sessions
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    if not app.config['SECRET_KEY']:
        print("❗ ERROR: SECRET_KEY is missing in .env")

    # SESSION config
    app.config['SESSION_TYPE'] = os.getenv('SESSION_TYPE', 'filesystem')

    # Init session system
    Session(app)

    # Register blueprints
    from server.blueprints import init_blueprints
    init_blueprints(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
