from datetime import datetime
from server.blueprints.services.feedback.model import FeedbackModel

class FeedbackService:

    @staticmethod
    def submit(data: dict):
        username = data.get("username")
        rating = data.get("rating")
        review = data.get("review")

        # Validate required fields
        if not username or not rating or not review:
            return {"success": False, "message": "Invalid data", "status": 400}

        # Prepare record for DB
        record = {
            "username": username,
            "rating": rating,
            "review": review,
            "created_at": datetime.utcnow()
        }

        FeedbackModel.create(record)

        return {"success": True, "message": "Feedback submitted successfully", "status": 200}
