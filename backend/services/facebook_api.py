import os, requests
from flask import request

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_TOKEN   = os.getenv("PAGE_ACCESS_TOKEN")

def verify_webhook():
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

def handle_messages():
    data = request.get_json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for ev in entry.get("messaging", []):
                sender_id = ev["sender"]["id"]
                if "message" in ev and "text" in ev["message"]:
                    text = ev["message"]["text"]
                    # aqui você salva no DB e gera resposta
                    from backend.database import SessionLocal
                    from backend.models import Message
                    from ai_engine import get_ai_response

                    db = SessionLocal()
                    msg = Message(sender=sender_id, content=text)
                    db.add(msg); db.commit(); db.refresh(msg); db.close()

                    reply = get_ai_response(text)
                    send_message(sender_id, reply)
    return "EVENT_RECEIVED", 200

def send_message(recipient_id: str, text: str):
    url = f"https://graph.facebook.com/v17.0/me/messages"
    payload = {
        "recipient": {"id": recipient_id},
        "message":   {"text": text}
    }
    params = {"access_token": PAGE_TOKEN}
    requests.post(url, params=params, json=payload)
