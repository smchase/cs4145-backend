from typing import Any, Dict, List

from flask import Blueprint, abort, jsonify, request
from sqlalchemy import func

from models import ClassificationQuestion, db

api = Blueprint("api", __name__)


@api.route("/")
def home() -> Dict[str, str]:
    return {"message": "Hello world"}


@api.route("/questions", methods=["GET"])
def get_questions() -> List[Dict[str, Any]]:
    questions = db.session.execute(db.select(ClassificationQuestion)).scalars()
    return jsonify([q.to_dict() for q in questions])


@api.route("/questions/<string:id>", methods=["GET"])
def get_question(id: str) -> Dict[str, Any]:
    if question := db.session.get(ClassificationQuestion, id):
        return question.to_dict()
    abort(404)


@api.route("/questions/random", methods=["GET"])
def get_random_question() -> Dict[str, Any]:
    if question := db.session.execute(
        db.select(ClassificationQuestion).order_by(func.random()).limit(1)
    ).scalar():
        return question.to_dict()
    abort(404)


@api.route("/questions", methods=["POST"])
def create_question() -> tuple[Dict[str, Any], int]:
    if not request.is_json:
        abort(400)

    data = request.get_json()
    required_fields = ["query", "context", "response"]
    if not all(field in data for field in required_fields):
        abort(400)

    question = ClassificationQuestion(**{k: data[k] for k in required_fields})
    db.session.add(question)
    db.session.commit()

    return question.to_dict(), 201


@api.route("/questions/<string:id>", methods=["PUT"])
def update_question(id: str) -> Dict[str, Any]:
    if not request.is_json:
        abort(400)

    if not (question := db.session.get(ClassificationQuestion, id)):
        abort(404)

    data = request.get_json()
    for field in ["query", "context", "response"]:
        if field in data:
            setattr(question, field, data[field])

    db.session.commit()
    return question.to_dict()


@api.route("/questions/<string:id>", methods=["DELETE"])
def delete_question(id: str) -> tuple[str, int]:
    if not (question := db.session.get(ClassificationQuestion, id)):
        abort(404)

    db.session.delete(question)
    db.session.commit()
    return "", 204
