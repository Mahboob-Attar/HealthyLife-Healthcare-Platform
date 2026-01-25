from flask import Flask
from server.blueprints import init_blueprints

def create_app():
    app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static"
    )

    # Register all blueprints
    init_blueprints(app)

    # Print URL map
    #print("\n📌 Registered Routes & Endpoints:\n", app.url_map, "\n")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
