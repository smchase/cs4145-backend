import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from flask import Flask, jsonify

from models import db
from routes import api


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    db_user = quote_plus(os.getenv("DB_USER"))
    db_pass = quote_plus(os.getenv("DB_PASSWORD"))
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{db_user}:{db_pass}" f"@{db_host}:{db_port}/{db_name}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
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
    app.run(debug=True)
