import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = os.getenv("HF_MODEL", "google/gemma-2-2b-it")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN missing in .env")


class ChatbotService:

    client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

    chat_history = [
        {"role": "system", "content": "You are a helpful virtual nurse. Provide short medical advice."}
    ]

    @staticmethod
    def respond(data):
        user_msg = data.get("message", "").strip()
        if not user_msg:
            return "Please enter a message."

        ChatbotService.chat_history.append({"role": "user", "content": user_msg})

        prompt = ""
        for msg in ChatbotService.chat_history:
            prompt += f"{msg['role']}: {msg['content']}\n"
        prompt += "assistant:"

        response = ChatbotService.client.text_generation(prompt, max_new_tokens=150, temperature=0.7)
        reply = response.strip()

        ChatbotService.chat_history.append({"role": "assistant", "content": reply})

        return reply
