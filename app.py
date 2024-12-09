import os
import uuid
from urllib.parse import quote_plus

from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{quote_plus(os.getenv('DB_USER'))}:{quote_plus(os.getenv('DB_PASSWORD'))}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class ClassificationQuestion(db.Model):
	id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
	query = db.Column(db.String(10000), nullable=False)
	context = db.Column(db.String(10000), nullable=False)
	response = db.Column(db.String(10000), nullable=False)

@app.route("/")
def home():
	return jsonify({"message": "Hello world"})

@app.route("/questions", methods=["GET"])
def get_questions():
    questions = db.session.execute(db.select(ClassificationQuestion)).scalars()
    return jsonify([{"id": question.id, "query": question.query, "context": question.context, "response": question.response} for question in questions])

@app.route("/questions/<string:id>", methods=["GET"])
def get_question(id):
    question = db.session.get(ClassificationQuestion, id)
    if not question:
        abort(404)
    return jsonify({
        "id": question.id,
        "query": question.query,
        "context": question.context,
        "response": question.response
    })

@app.route("/questions/random", methods=["GET"])
def get_random_question():
    question = db.session.execute(
        db.select(ClassificationQuestion).order_by(func.random()).limit(1)
    ).scalar()
    if not question:
        abort(404)
    return jsonify({
        "id": question.id,
        "query": question.query,
        "context": question.context,
        "response": question.response
    })

@app.route("/questions", methods=["POST"])
def create_question():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    
    required_fields = ["query", "context", "response"]
    if not all(field in data for field in required_fields):
        abort(400)
    
    question = ClassificationQuestion(
        query=data["query"],
        context=data["context"],
        response=data["response"]
    )
    db.session.add(question)
    db.session.commit()
    
    return jsonify({
        "id": question.id,
        "query": question.query,
        "context": question.context,
        "response": question.response
    }), 201

@app.route("/questions/<string:id>", methods=["PUT"])
def update_question(id):
    if not request.is_json:
        abort(400)
    
    question = db.session.get(ClassificationQuestion, id)
    if not question:
        abort(404)
    
    data = request.get_json()
    if "query" in data:
        question.query = data["query"]
    if "context" in data:
        question.context = data["context"]
    if "response" in data:
        question.response = data["response"]
    
    db.session.commit()
    return jsonify({
        "id": question.id,
        "query": question.query,
        "context": question.context,
        "response": question.response
    })

@app.route("/questions/<string:id>", methods=["DELETE"])
def delete_question(id):
    question = db.session.get(ClassificationQuestion, id)
    if not question:
        abort(404)
    
    db.session.delete(question)
    db.session.commit()
    return "", 204

if __name__ == "__main__":
	app.run(debug=True)
