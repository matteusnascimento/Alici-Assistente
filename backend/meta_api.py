import requests
import os
from models import save_message

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
API_URL = "https://graph.facebook.com/v19.0/me/messages"

def send_message(recipient_id, message):
    payload = {
        "messaging_type": "RESPONSE",
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    return response.json()

def handle_meta_webhook(data):
    if "entry" in data:
        for entry in data["entry"]:
            for messaging in entry.get("messaging", []):
                sender_id = messaging["sender"]["id"]
                if "message" in messaging:
                    message_text = messaging["message"].get("text", "")
                    save_message(sender_id, message_text, "user")
                    send_message(sender_id, "Mensagem recebida! Alici está aprendendo.")
                    save_message("Alici", "Mensagem recebida! Alici está aprendendo.", "bot")
