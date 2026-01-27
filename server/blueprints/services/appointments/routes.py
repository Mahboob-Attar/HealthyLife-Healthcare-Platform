from flask import Blueprint, request, render_template, jsonify, session
from server.blueprints.services.appointments.service import AppointmentService

appointments = Blueprint("appointments", __name__, url_prefix="/appointments")

@appointments.route("/", methods=["GET"])
def appointment_page():
    role = session.get("role")
    user_id = session.get("user_id")

    if not role or not user_id:
        return "Unauthorized", 401

    if role == "patient":
        selected_city = request.args.get("city")
        data = AppointmentService.load_appointment_page(selected_city)
        return render_template("appointments/patient_view.html", **data)

    elif role == "doctor":
        data = AppointmentService.doctor_load_dashboard(user_id)
        return render_template("appointments/doctor_view.html", **data)

    else:
        return "Unknown role", 400


# ---- Patient APIs ----
@appointments.route("/book", methods=["POST"])
def book():
    return jsonify(AppointmentService.patient_book(request.json))

@appointments.route("/cancel/<int:id>", methods=["DELETE"])
def cancel(id):
    return jsonify(AppointmentService.patient_cancel(id))


# ---- Doctor APIs ----
@appointments.route("/update", methods=["POST"])
def update():
    return jsonify(AppointmentService.doctor_update_status(request.json))

@appointments.route("/reschedule", methods=["POST"])
def reschedule():
    return jsonify(AppointmentService.doctor_reschedule(request.json))
