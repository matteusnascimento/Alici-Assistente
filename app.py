### app.py
```python
import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from backend.database import SessionLocal, engine
from backend.models import Base, Message
from ai_engine import get_ai_response
from backend.services.facebook_api import verify_webhook, handle_messages

# carrega .env
load_dotenv()
# cria tabelas
Base.metadata.create_all(bind=engine)

app = Flask(__name__, template_folder="templates")

# Rota de interface web (painel admin ou landing)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/admin", methods=["GET"])
def admin_panel():
    db = SessionLocal()
    msgs = db.query(Message).order_by(Message.id.desc()).all()
    db.close()
    return render_template("admin.html", messages=msgs)

# Webhook do Facebook
@app.route("/webhook", methods=["GET","POST"])
def webhook():
    if request.method == "GET":
        return verify_webhook()
    else:
        return handle_messages()

# API interna de conversas
@app.route("/api/message", methods=["POST"])
def api_message():
    data = request.json
    db = SessionLocal()
    msg = Message(sender=data["sender"], content=data["message"])
    db.add(msg); db.commit(); db.refresh(msg); db.close()

    response = get_ai_response(data["message"])
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
