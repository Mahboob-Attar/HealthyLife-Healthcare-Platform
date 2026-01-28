from server.blueprints.services.home.routes import home_bp
from server.blueprints.services.doctors.routes import doctors
from server.blueprints.services.appointments.routes import appointments
from server.blueprints.services.feedback.routes import feedback_bp
from server.blueprints.services.aiml.diagnostic.routes import diagnostic_bp
from server.blueprints.services.aiml.chatbot.routes import chatbot_bp
from server.blueprints.services.admin.routes import admin_bp
from server.blueprints.services.auth.routes import auth

def init_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(doctors)
    app.register_blueprint(appointments)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(diagnostic_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth)
