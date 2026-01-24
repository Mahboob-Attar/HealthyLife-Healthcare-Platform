import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from services.doctors.model import DoctorModel

UPLOAD_FOLDER = "uploads/doctors"
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif"}


class DoctorService:

    @staticmethod
    def get_image_path():
        return UPLOAD_FOLDER

    @staticmethod
    def register(request):
        try:
            name = request.form.get("name")
            phone = request.form.get("phone")
            email = request.form.get("email")
            experience = request.form.get("experience")
            specialization = request.form.get("specialization")
            services = request.form.get("services")
            clinic = request.form.get("clinic")
            location = request.form.get("location")
            photo = request.files.get("photo")

            # Validate required fields
            if not all([name, phone, email, specialization, photo]):
                return {"success": False, "message": "Missing required fields", "status": 400}

            # Check duplicates
            if DoctorModel.find_by_email(email):
                return {"success": False, "message": "Email already registered", "status": 409}

            if DoctorModel.find_by_phone(phone):
                return {"success": False, "message": "Phone already registered", "status": 409}

            # Validate file extension
            ext = photo.filename.rsplit(".", 1)[1].lower()
            if ext not in ALLOWED_EXT:
                return {"success": False, "message": "Invalid file type", "status": 400}

            # Ensure upload directory exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            # Save image
            unique_name = f"{uuid.uuid4().hex}.{ext}"
            filename = secure_filename(unique_name)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            photo.save(file_path)

            # Insert into DB
            DoctorModel.create({
                "name": name,
                "phone": phone,
                "email": email,
                "experience": experience,
                "specialization": specialization,
                "services": services,
                "clinic": clinic,
                "location": location,
                "photo_path": filename,
                "created_at": datetime.now()
            })

            return {"success": True, "message": "Doctor registered successfully", "status": 200}

        except Exception as e:
            print("❌ DoctorService.register Error:", e)
            return {"success": False, "message": "Server Error", "status": 500}

    @staticmethod
    def get_all():
        try:
            doctors = DoctorModel.get_all()
            for doc in doctors:
                doc["photo_path"] = doc.get("photo_path") or "default.jpg"
            return doctors
        except Exception as e:
            print("❌ DoctorService.get_all Error:", e)
            return []
