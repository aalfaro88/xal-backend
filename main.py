import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes.stackexchange import stack_exchange
from app.models.flight_model import db  # pylint: disable=no-name-in-module
from app.routes.flight_data import (
    data_bp,
)  # Import the blueprint for flight data routes

# Load environment variables
load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load configuration values
    app.config["CLIENT_ID"] = os.getenv("CLIENT_ID")
    app.config["KEY"] = os.getenv("KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "mysql+pymysql://root:ironhack@localhost/airplane_database",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(data_bp, url_prefix="/data")  # Register flight data routes
    app.register_blueprint(stack_exchange, url_prefix="/stackexchange")

    return app


app = create_app()

if __name__ == "__main__":
    port = os.getenv("FLASK_RUN_PORT", "5001")
    app.run(host="0.0.0.0", port=int(port), debug=True)
