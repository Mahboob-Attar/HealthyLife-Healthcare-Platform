from flask import Blueprint, render_template


appointment_bp = Blueprint('appointment', __name__,url_prefix="/appointment")

@appointment_bp.route('/appointment')
def appointment():
    return render_template('appointment.html')
