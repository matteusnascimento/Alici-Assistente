import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# importa Base (metadata) e engine/SessionLocal do database.py
from backend.database import Base, SessionLocal, engine
# importa a classe Message do models.py
from backend.models import Message

from ai_engine import get_ai_response
from backend.services.facebook_api import verify_webhook, handle_messages

# carrega variáveis de ambiente de .env
load_dotenv()

# cria as tabelas no banco se ainda não existirem
Base.metadata.create_all(bind=engine)

# define o app Flask e as pastas
app = Flask(__name__, template_folder='backend/templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/admin", methods=["GET"])
def admin_panel():
    db = SessionLocal()
    msgs = db.query(Message).order_by(Message.id.desc()).all()
    db.close()
    return render_template("admin.html", messages=msgs)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return verify_webhook()
    return handle_messages()

@app.route("/api/message", methods=["POST"])
def api_message():
    data = request.json or {}
    sender = data.get("sender", "Usuário")
    message = data.get("message", "")

    if not message.strip():
        return jsonify({"response": "Digite uma mensagem válida."})

    db = SessionLocal()
    msg = Message(sender=sender, content=message)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    db.close()

    response = get_ai_response(message)
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
