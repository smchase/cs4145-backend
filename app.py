import uuid
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

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
    return jsonify([{"query": question.query, "context": question.context, "response": question.response} for question in questions])

if __name__ == "__main__":
	app.run(debug=True)
