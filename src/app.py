import logging
import os
from logging.handlers import RotatingFileHandler
from urllib.parse import quote_plus

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from models import db
from routes import api


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    # Configure logging
    if not os.path.exists("logs"):
        os.makedirs("logs")

    file_handler = RotatingFileHandler("logs/app.log", maxBytes=10240, backupCount=10)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Also log to stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("Application startup")

    # Database configuration
    db_user = quote_plus(os.getenv("DB_USER"))
    db_pass = quote_plus(os.getenv("DB_PASSWORD"))
    db_name = os.getenv("DB_NAME")

    socket_path = os.getenv("DB_SOCKET_PATH")
    if socket_path:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"postgresql://{db_user}:{db_pass}@/{db_name}" f"?host={socket_path}"
        )
    else:
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"postgresql://{db_user}:{db_pass}" f"@{db_host}:{db_port}/{db_name}"
        )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(api)

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(error="Bad Request"), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error="Not Found"), 404

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
