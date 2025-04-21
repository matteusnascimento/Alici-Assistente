
from flask import Flask, request, jsonify
from backend.database import SessionLocal, engine
from backend.models import Base, Message
from ai_engine import get_ai_response

Base.metadata.create_all(bind=engine)

app = Flask(__name__)

@app.route("/api/message", methods=["POST"])
def handle_message():
    data = request.json
    db = SessionLocal()
    msg = Message(sender=data["sender"], content=data["message"])
    db.add(msg)
    db.commit()
    db.refresh(msg)
    db.close()
    response = get_ai_response(data["message"])
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
