from flask import Blueprint, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load the environment variables from your apikey.env
dotenv_path = os.path.join(os.path.dirname(__file__), "apikey.env")
load_dotenv(dotenv_path)

# Fetch API key and model name
HF_API_KEY = os.getenv("HF_TOKEN")   # Must match HF_TOKEN in apikey.env
HF_MODEL = os.getenv("HF_MODEL", "gpt2")

print("HF_API_KEY loaded:", HF_API_KEY is not None)
print("HF_MODEL:", HF_MODEL)

HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")

# Chatbot page
@chatbot_bp.route("/")
def chatbot():
    return render_template("chatbot.html")

# Chatbot API endpoint
@chatbot_bp.route("/get_response", methods=["POST"])
def get_response():
    try:
        data = request.get_json()
        user_msg = data.get("message", "").strip()

        if not user_msg:
            return jsonify({"response": "Please enter a message."})

        payload = {"inputs": user_msg}
        response = requests.post(HF_API_URL, headers=HEADERS, json=payload, timeout=30)

        try:
            result = response.json()
        except ValueError:
            return jsonify({"response": "⚠️ API Error: Invalid response from Hugging Face"})

        # Extract generated text
        if isinstance(result, list) and "generated_text" in result[0]:
            bot_reply = result[0]["generated_text"]
        else:
            bot_reply = str(result)

        return jsonify({"response": bot_reply})

    except requests.exceptions.HTTPError as http_err:
        return jsonify({"response": f"⚠️ HTTP Error: {http_err}"})
    except Exception as e:
        return jsonify({"response": f"⚠️ Error: {str(e)}"})
