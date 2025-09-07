from .home import home_bp
from .diagnostics import diagnostics_bp
from .pharmacy import pharmacy_bp
from .labtest import labtest_bp
from .chatbot import chatbot_bp

def init_blueprints(app):
    """Register all blueprints here"""
    app.register_blueprint(home_bp)
    app.register_blueprint(diagnostics_bp)
    app.register_blueprint(pharmacy_bp)
    app.register_blueprint(labtest_bp)
    app.register_blueprint(chatbot_bp)
