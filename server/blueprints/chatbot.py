from flask import Blueprint, render_template, request, jsonify
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path)

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = os.getenv("HF_MODEL", "google/gemma-2-2b-it")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN missing in .env")

# IMPORTANT: Define blueprint BEFORE using it
chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")

# HF Client
client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

# Chat history
chat_history = [
    {"role": "system", "content": "You are a helpful virtual nurse. Provide friendly, short medical advice."}
]

# Routes below

@chatbot_bp.route("/")
def chatbot():
    return render_template("chatbot.html")


@chatbot_bp.route("/get_response", methods=["POST"])
def get_response():
    try:
        data = request.get_json()
        user_msg = data.get("message", "").strip()
        if not user_msg:
            return jsonify({"response": "Please enter a message."})

        chat_history.append({"role": "user", "content": user_msg})

        prompt = ""
        for msg in chat_history:
            prompt += f"{msg['role']}: {msg['content']}\n"
        prompt += "assistant:"

        response = client.text_generation(
            prompt,
            max_new_tokens=150,
            temperature=0.7
        )
        bot_reply = response.strip()

        chat_history.append({"role": "assistant", "content": bot_reply})
        return jsonify({"response": bot_reply})

    except Exception as e:
        import traceback
        print("\n❌ BACKEND ERROR:")
        traceback.print_exc()
        return jsonify({"response": "⚠️ Something went wrong. Please try again."})
