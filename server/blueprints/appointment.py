from flask import Blueprint, render_template

# Create a separate Blueprint for appointment portal
appointment_bp = Blueprint('appointment', __name__,url_prefix="/appointment")

@appointment_bp.route('/appointment')
def appointment_portal():
    return render_template('appointment.html')
