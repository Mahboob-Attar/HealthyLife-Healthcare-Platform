from flask import Flask
from blueprints import init_blueprints

# Flask App Initialization
app = Flask(__name__)

# Register All Blueprints
init_blueprints(app)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
