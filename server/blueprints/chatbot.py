from flask import Blueprint, render_template, request, jsonify

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")

# Chatbot Page
@chatbot_bp.route("/")
def chatbot():
    return render_template("chatbot.html")

# Chatbot API

# @chatbot_bp.route("/get_response", methods=["POST"])
# def get_response():
#     try:
#         data = request.get_json()
#         user_msg = data.get("message", "").lower()

#         # Dummy logic replace with real logic 
#         if user_msg in ["hi", "hello", "hey"]:
#             bot_reply = "Hello! 👋 How can I help you today?"
#         elif "health" in user_msg:
#             bot_reply = "I can assist you with health-related information 🩺"
#         elif "bye" in user_msg:
#             bot_reply = "Goodbye! Have a great day 😊"
#         else:
#             bot_reply = "I'm still learning 🤖. Can you rephrase?"

#         return jsonify({"response": bot_reply})
    
#     except Exception as e:
#         return jsonify({"response": f"⚠️ Error: {str(e)}"})
