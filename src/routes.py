from typing import Any, Dict, List

from flask import Blueprint, abort, current_app, jsonify, request
from sqlalchemy import func

from models import ClassificationQuestion, Counter, UserResponse, db

api = Blueprint("api", __name__)


@api.route("/")
def home() -> Dict[str, str]:
    current_app.logger.info("Home endpoint accessed")
    return {"message": "Hello world"}


@api.route("/questions", methods=["GET"])
def get_questions() -> List[Dict[str, Any]]:
    current_app.logger.info("Fetching all questions")
    questions = db.session.execute(db.select(ClassificationQuestion)).scalars()
    questions_list = [q.to_dict() for q in questions]
    current_app.logger.info(f"Retrieved {len(questions_list)} questions")
    return jsonify(questions_list)


@api.route("/questions/<string:id>", methods=["GET"])
def get_question(id: str) -> Dict[str, Any]:
    current_app.logger.info(f"Fetching question with id: {id}")
    if question := db.session.get(ClassificationQuestion, id):
        current_app.logger.info(f"Found question {id}")
        return question.to_dict()
    current_app.logger.warning(f"Question {id} not found")
    abort(404)


@api.route("/questions/random", methods=["GET"])
def get_random_question() -> Dict[str, Any]:
    current_app.logger.info("Fetching random question")
    if question := db.session.execute(
        db.select(ClassificationQuestion).order_by(func.random()).limit(1)
    ).scalar():
        current_app.logger.info(f"Retrieved random question {question.id}")
        return question.to_dict()
    current_app.logger.warning("No questions available for random selection")
    abort(404)


@api.route("/questions", methods=["POST"])
def create_question() -> tuple[Dict[str, Any], int]:
    if not request.is_json:
        current_app.logger.warning("Received non-JSON request for question creation")
        abort(400)

    data = request.get_json()
    required_fields = ["query", "context1", "context2", "response"]
    if not all(field in data for field in required_fields):
        current_app.logger.warning(
            "Missing required fields in question creation:"
            f"{[f for f in required_fields if f not in data]}"
        )
        abort(400)

    question = ClassificationQuestion(**{k: data[k] for k in required_fields})
    db.session.add(question)
    db.session.commit()
    current_app.logger.info(f"Created new question with id: {question.id}")

    return question.to_dict(), 201


@api.route("/questions/<string:id>", methods=["PUT"])
def update_question(id: str) -> Dict[str, Any]:
    current_app.logger.info(f"Attempting to update question {id}")
    if not request.is_json:
        current_app.logger.warning(
            f"Received non-JSON request for question update {id}"
        )
        abort(400)

    if not (question := db.session.get(ClassificationQuestion, id)):
        current_app.logger.warning(f"Question {id} not found for update")
        abort(404)

    data = request.get_json()
    for field in ["query", "context1", "context2", "response"]:
        if field in data:
            setattr(question, field, data[field])

    db.session.commit()
    current_app.logger.info(f"Successfully updated question {id}")
    return question.to_dict()


@api.route("/questions/<string:id>", methods=["DELETE"])
def delete_question(id: str) -> tuple[str, int]:
    current_app.logger.info(f"Attempting to delete question {id}")
    if not (question := db.session.get(ClassificationQuestion, id)):
        current_app.logger.warning(f"Question {id} not found for deletion")
        abort(404)

    db.session.delete(question)
    db.session.commit()
    current_app.logger.info(f"Successfully deleted question {id}")
    return "", 204


@api.route("/responses", methods=["GET"])
def get_responses() -> List[Dict[str, Any]]:
    current_app.logger.info("Fetching all responses")
    responses = db.session.execute(db.select(UserResponse)).scalars()
    responses_list = [r.to_dict() for r in responses]
    current_app.logger.info(f"Retrieved {len(responses_list)} responses")
    return jsonify(responses_list)


@api.route("/responses", methods=["POST"])
def create_response() -> tuple[Dict[str, Any], int]:
    if not request.is_json:
        current_app.logger.warning("Received non-JSON request for response creation")
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
        current_app.logger.warning(
            "Missing required fields in response creation:"
            f"{[f for f in required_fields if f not in data]}"
        )
        abort(400)

    # Verify question exists
    if not db.session.get(ClassificationQuestion, data["question_id"]):
        current_app.logger.warning(
            f"Question {data['question_id']} not found for response creation"
        )
        abort(404, description="Question not found")

    # Create response with optional comments field
    response_data = {k: data[k] for k in required_fields}
    if "comments" in data:
        response_data["comments"] = data["comments"]

    response = UserResponse(**response_data)
    db.session.add(response)
    db.session.commit()
    current_app.logger.info(
        "Created new response for question"
        f"{data['question_id']} by worker {data['worker_id']}"
    )

    return response.to_dict(), 201


@api.route("/counter", methods=["GET"])
def get_counter() -> Dict[str, Any]:
    current_app.logger.info("Fetching counter value")
    counter = db.session.execute(db.select(Counter).where(Counter.id == 1)).scalar()
    if not counter:
        counter = Counter(id=1, value=0)
        db.session.add(counter)
        db.session.commit()
        current_app.logger.info("Initialized new counter with value 0")
    else:
        current_app.logger.info(f"Retrieved counter value: {counter.value}")
    return counter.to_dict()


@api.route("/counter/increment", methods=["POST"])
def increment_counter() -> Dict[str, Any]:
    current_app.logger.info("Incrementing counter")
    counter = db.session.execute(db.select(Counter).where(Counter.id == 1)).scalar()
    if not counter:
        counter = Counter(id=1, value=0)
        db.session.add(counter)
        current_app.logger.info("Initialized new counter")
    counter.value += 1
    db.session.commit()
    current_app.logger.info(f"Counter incremented to {counter.value}")
    return counter.to_dict()
