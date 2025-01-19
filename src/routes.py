from typing import Any, Dict, List

from flask import Blueprint, abort, jsonify, request
from sqlalchemy import func

from models import ClassificationQuestion, Counter, UserResponse, db

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
    required_fields = ["query", "context1", "context2", "response"]
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
    for field in ["query", "context1", "context2", "response"]:
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


@api.route("/responses", methods=["GET"])
def get_responses() -> List[Dict[str, Any]]:
    responses = db.session.execute(db.select(UserResponse)).scalars()
    return jsonify([r.to_dict() for r in responses])


@api.route("/responses", methods=["POST"])
def create_response() -> tuple[Dict[str, Any], int]:
    if not request.is_json:
        abort(400)

    data = request.get_json()
    required_fields = [
        "question_id",
        "worker_id",
        "is_faithful",
        "is_relevant",
        "faithfulness",
        "relevance",
    ]
    if not all(field in data for field in required_fields):
        abort(400)

    # Verify question exists
    if not db.session.get(ClassificationQuestion, data["question_id"]):
        abort(404, description="Question not found")

    # Create response with optional comments field
    response_data = {k: data[k] for k in required_fields}
    if "comments" in data:
        response_data["comments"] = data["comments"]

    response = UserResponse(**response_data)
    db.session.add(response)
    db.session.commit()

    return response.to_dict(), 201


@api.route("/counter", methods=["GET"])
def get_counter() -> Dict[str, Any]:
    counter = db.session.execute(db.select(Counter).where(Counter.id == 1)).scalar()
    if not counter:
        counter = Counter(id=1, value=0)
        db.session.add(counter)
        db.session.commit()
    return counter.to_dict()


@api.route("/counter/increment", methods=["POST"])
def increment_counter() -> Dict[str, Any]:
    counter = db.session.execute(db.select(Counter).where(Counter.id == 1)).scalar()
    if not counter:
        counter = Counter(id=1, value=0)
        db.session.add(counter)
    counter.value += 1
    db.session.commit()
    return counter.to_dict()
