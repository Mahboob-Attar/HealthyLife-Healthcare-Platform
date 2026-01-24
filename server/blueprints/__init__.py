# server/blueprints/__init__.py

from services.home.routes import home_bp
from services.doctors.routes import doctors_bp
from services.appointments.routes import appointments_bp
from services.feedback.routes import feedback_bp
from services.aiml.diagnostic.routes import diagnostic_bp
from services.aiml.chatbot.routes import chatbot_bp
from services.admin.routes import admin_bp  

def init_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(diagnostic_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(admin_bp)  
