# app.py

from flask import Flask, request, jsonify
from meta_api import handle_meta_webhook
from db import init_db
from models import save_message

app = Flask(__name__)
init_db()

@app.route("/", methods=["GET"])
def home():
    return "Alici Backend Ativo"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return request.args.get("hub.challenge")
    elif request.method == "POST":
        data = request.get_json()
        handle_meta_webhook(data)
        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(port=5000)
