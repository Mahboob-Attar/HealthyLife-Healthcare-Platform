import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import render_template

from server.blueprints.services.doctors.model import DoctorModel
from server.config.email import send_email_html

UPLOAD_FOLDER = "uploads/doctors"
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif"}


class DoctorService:

    @staticmethod
    def get_image_path():
        return UPLOAD_FOLDER

    @staticmethod
    def register(request):
        try:
            # Form data
            name = request.form.get("name")
            phone = request.form.get("phone")
            email = request.form.get("email")
            license_email = request.form.get("license")
            specialization = request.form.get("specialization")
            experience = request.form.get("experience")
            services = request.form.get("services")
            clinic = request.form.get("clinic")
            location = request.form.get("location")
            photo = request.files.get("photo")

            user_id = request.form.get("user_id")  # optional

            # Validation
            if not all([
                name, phone, email, license_email,
                specialization, experience, clinic,
                location, services, photo
            ]):
                return {
                    "success": False,
                    "message": "Missing required fields",
                    "status": 400
                }

            if DoctorModel.find_by_email(email):
                return {"success": False, "message": "Email already registered", "status": 409}

            if DoctorModel.find_by_phone(phone):
                return {"success": False, "message": "Phone already registered", "status": 409}

            if DoctorModel.find_by_license(license_email):
                return {"success": False, "message": "License already registered", "status": 409}

            # Image validation
            if "." not in photo.filename:
                return {"success": False, "message": "Invalid image file", "status": 400}

            ext = photo.filename.rsplit(".", 1)[1].lower()
            if ext not in ALLOWED_EXT:
                return {"success": False, "message": "Invalid image type", "status": 400}

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(f"{uuid.uuid4().hex}.{ext}")
            photo_path = os.path.join(UPLOAD_FOLDER, filename)
            photo.save(photo_path)

            # Save to DB (CRITICAL)
            created = DoctorModel.create({
                "user_id": user_id,
                "name": name,
                "phone": phone,
                "email": email,
                "license_email": license_email,
                "experience": experience,
                "specialization": specialization,
                "services": services,
                "clinic": clinic,
                "location": location,
                "photo_path": filename
            })

            if not created:
                # rollback file if DB insert failed
                if os.path.exists(photo_path):
                    os.remove(photo_path)

                return {
                    "success": False,
                    "message": "Doctor registration failed",
                    "status": 500
                }

           
            # Send confirmation email
            html = render_template(
                "emails/doctor_registration_email.html",
                doctor_name=name,
                specialization=specialization,
                clinic=clinic,
                location=location,
                experience=experience,
                year=datetime.now().year
            )

            send_email_html(
                email,
                "HealthyLife – Doctor Registration Received",
                html
            )

            return {
                "success": True,
                "message": "Doctor registration submitted successfully",
                "status": 200
            }

        except Exception as e:
            print("❌ DoctorService.register Error:", e)
            return {
                "success": False,
                "message": "Internal Server Error",
                "status": 500
            }
