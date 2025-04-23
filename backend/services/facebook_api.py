from flask import request, jsonify
import requests, os

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_TOKEN   = os.getenv("PAGE_ACCESS_TOKEN")

def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

def handle_messages():
    data = request.get_json()
    # percorre callbacks, extrai sender id e texto, chama AI e envia resposta
    return "EVENT_RECEIVED", 200

def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v17.0/me/messages"
    payload = {"recipient":{"id":recipient_id},"message":{"text":text}}
    requests.post(url, params={"access_token":PAGE_TOKEN}, json=payload)
