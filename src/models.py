import uuid
from typing import Any, Dict

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ClassificationQuestion(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    query = db.Column(db.String(10000), nullable=False)
    context = db.Column(db.String(10000), nullable=False)
    response = db.Column(db.String(10000), nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "query": self.query,
            "context": self.context,
            "response": self.response,
        }
