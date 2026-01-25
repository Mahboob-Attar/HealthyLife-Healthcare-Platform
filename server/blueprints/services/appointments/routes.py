from flask import Blueprint, request, render_template, jsonify
from server.blueprints.services.appointments.service import AppointmentService

appointments_bp = Blueprint("appointments_bp", __name__, url_prefix="/appointments")


@appointments_bp.route("/", methods=["GET"])
def appointment_page():
    """
    Render the appointment page with doctor list + city filters
    """
    try:
        selected_city = request.args.get("city")
        response = AppointmentService.load_appointment_page(selected_city)

        return render_template(
            "appointment.html",
            doctors=response["doctors"],
            cities=response["cities"],
            selected_city=selected_city
        )

    except Exception as e:
        print("❌ Appointment Page Error:", e)
        return "Internal Server Error", 500
