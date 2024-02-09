import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import OperationalError
from time import sleep

# Assuming this path is correct
from app.models.flight_model import db, Aerolineas, Aeropuertos, Movimientos, Vuelos
from app.routes.flight_data import data_bp
from app.routes.stackexchange import stack_exchange

# Load environment variables
load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load configuration values
    app.config["CLIENT_ID"] = os.getenv("CLIENT_ID")
    app.config["KEY"] = os.getenv("KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)

    with app.app_context():
        # Implement retry logic
        max_retries = 5
        retry_count = 0

        while retry_count < max_retries:
            try:
                engine = db.get_engine(app, bind=None)
                if not database_exists(engine.url):  # Checks if database exists
                    create_database(engine.url)  # Creates database if it does not exist
                    print("Database created.")
                db.create_all()  # Attempt to create tables, will silently fail if tables already exist
                break  # Break out of the loop if successful
            except OperationalError as e:
                print(
                    f"Database connection failed. Retrying... ({retry_count + 1}/{max_retries})"
                )
                sleep(5)  # Wait for 5 seconds before retrying
                retry_count += 1

        if retry_count == max_retries:
            print("Failed to connect to the database after several retries.")
            raise OperationalError("Could not connect to the database.")

        # Function to populate tables if they're found to be empty
        def populate_tables():
            # Check and populate Aerolineas if empty
            if not Aerolineas.query.first():
                aerolineas = [
                    Aerolineas(id_aerolinea=1, nombre_aerolinea="Volaris"),
                    Aerolineas(id_aerolinea=2, nombre_aerolinea="Aeromar"),
                    Aerolineas(id_aerolinea=3, nombre_aerolinea="Interjet"),
                    Aerolineas(id_aerolinea=4, nombre_aerolinea="Aeromexico"),
                ]
                db.session.add_all(aerolineas)

            # Check and populate Aeropuertos if empty
            if not Aeropuertos.query.first():
                aeropuertos = [
                    Aeropuertos(id_aeropuerto=1, nombre_aeropuerto="Benito Juarez"),
                    Aeropuertos(id_aeropuerto=2, nombre_aeropuerto="Guanajuato"),
                    Aeropuertos(id_aeropuerto=3, nombre_aeropuerto="La Paz"),
                    Aeropuertos(id_aeropuerto=4, nombre_aeropuerto="Oaxaca"),
                ]
                db.session.add_all(aeropuertos)

            # Check and populate Movimientos if empty
            if not Movimientos.query.first():
                movimientos = [
                    Movimientos(id_movimiento=1, descripcion="Salida"),
                    Movimientos(id_movimiento=2, descripcion="Llegada"),
                ]
                db.session.add_all(movimientos)

            # Check and populate Vuelos if empty
            if not Vuelos.query.first():
                vuelos = [
                    Vuelos(
                        id_aerolinea=1,
                        id_aeropuerto=1,
                        id_movimiento=1,
                        dia="2021-05-02",
                    ),
                    Vuelos(
                        id_aerolinea=2,
                        id_aeropuerto=1,
                        id_movimiento=1,
                        dia="2021-05-02",
                    ),
                    Vuelos(
                        id_aerolinea=3,
                        id_aeropuerto=2,
                        id_movimiento=2,
                        dia="2021-05-02",
                    ),
                    Vuelos(
                        id_aerolinea=4,
                        id_aeropuerto=3,
                        id_movimiento=2,
                        dia="2021-05-02",
                    ),
                    Vuelos(
                        id_aerolinea=1,
                        id_aeropuerto=3,
                        id_movimiento=2,
                        dia="2021-05-02",
                    ),
                    Vuelos(
                        id_aerolinea=2,
                        id_aeropuerto=1,
                        id_movimiento=1,
                        dia="2021-05-02",
                    ),
                    Vuelos(
                        id_aerolinea=2,
                        id_aeropuerto=3,
                        id_movimiento=1,
                        dia="2021-05-04",
                    ),
                    Vuelos(
                        id_aerolinea=3,
                        id_aeropuerto=4,
                        id_movimiento=1,
                        dia="2021-05-04",
                    ),
                    Vuelos(
                        id_aerolinea=3,
                        id_aeropuerto=4,
                        id_movimiento=2,
                        dia="2021-05-04",
                    ),
                ]
                db.session.add_all(vuelos)

            db.session.commit()

        # Call populate_tables after db.create_all()
        populate_tables()
        print("Tables populated if they were empty.")

    # Register blueprints
    app.register_blueprint(data_bp, url_prefix="/data")
    app.register_blueprint(stack_exchange, url_prefix="/stackexchange")

    return app


app = create_app()

if __name__ == "__main__":
    port = os.getenv("FLASK_RUN_PORT", "5001")
    app.run(host="0.0.0.0", port=int(port), debug=True)
