import uuid
from datetime import UTC, datetime
from typing import Any, Dict

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ClassificationQuestion(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    query = db.Column(db.String(10000), nullable=False)
    context1 = db.Column(db.String(10000), nullable=False)
    context2 = db.Column(db.String(10000), nullable=False)
    response = db.Column(db.String(10000), nullable=False)
    responses = db.relationship("UserResponse", backref="question", lazy=True)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "query": self.query,
            "context1": self.context1,
            "context2": self.context2,
            "response": self.response,
        }


class UserResponse(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id = db.Column(
        db.String(36), db.ForeignKey("classification_question.id"), nullable=False
    )
    time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    worker_id = db.Column(db.String(24), nullable=False)
    is_faithful = db.Column(db.Boolean, nullable=False)
    is_relevant = db.Column(db.Boolean, nullable=False)
    faithfulness = db.Column(db.String(1000), nullable=False)
    relevance = db.Column(db.String(1000), nullable=False)
    comments = db.Column(db.String(1000))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "question_id": self.question_id,
            "time": self.time.isoformat(),
            "worker_id": self.worker_id,
            "is_faithful": self.is_faithful,
            "is_relevant": self.is_relevant,
            "faithfulness": self.faithfulness,
            "relevance": self.relevance,
            "comments": self.comments,
        }
