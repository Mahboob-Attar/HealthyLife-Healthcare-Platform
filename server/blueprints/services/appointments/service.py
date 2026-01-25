from server.blueprints.services.appointments.model import AppointmentModel

class AppointmentService:

    @staticmethod
    def load_appointment_page(selected_city=None):
        """
        Logic for loading doctors + cities for appointment page
        """
        # Load distinct cities
        cities = AppointmentModel.get_all_cities()

        # Load doctors (filtered or all)
        if selected_city:
            doctors = AppointmentModel.get_doctors_by_city(selected_city)
        else:
            doctors = AppointmentModel.get_all_doctors()

        # Assign default images
        for doc in doctors:
            doc["photo_path"] = doc.get("photo_path") or "default.jpg"

        return {
            "cities": cities,
            "doctors": doctors
        }
