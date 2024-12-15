from src.app import create_app
from src.models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database initialized successfully.")
