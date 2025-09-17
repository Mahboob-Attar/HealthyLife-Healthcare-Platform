from .home import home_bp
from .diagnostics import diagnostics_bp
from .dashboard import dashboard_bp
from .chatbot import chatbot_bp
from .appointment import appointment_bp
from .doctorRegistration import doctor_bp

def init_blueprints(app):
    """Register all blueprints here"""
    app.register_blueprint(home_bp)
    app.register_blueprint(diagnostics_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(doctor_bp)
