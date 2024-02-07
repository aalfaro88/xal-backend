from flask import Blueprint, jsonify
from ..models.flight_model import Aerolineas, Aeropuertos, Movimientos, Vuelos

data_bp = Blueprint("data_routes", __name__)


@data_bp.route("/aerolineas", methods=["GET"])
def get_aerolineas():
    """
    Retrieve a list of all aerolineas (airlines) from the database, including their IDs and names.

    Returns:
        A JSON list of all airlines, each represented by a dictionary containing the airline's ID and name.
    """
    all_aerolineas = Aerolineas.query.all()
    return jsonify(
        [
            {"id": aerolinea.id_aerolinea, "nombre": aerolinea.nombre_aerolinea}
            for aerolinea in all_aerolineas
        ]
    )


@data_bp.route("/aeropuertos", methods=["GET"])
def get_aeropuertos():
    """
    Retrieve a list of all aeropuertos (airports) from the database, including their IDs and names.

    Returns:
        A JSON list of all airports, each represented by a dictionary containing the airport's ID and name.
    """
    all_aeropuertos = Aeropuertos.query.all()
    return jsonify(
        [
            {"id": aeropuerto.id_aeropuerto, "nombre": aeropuerto.nombre_aeropuerto}
            for aeropuerto in all_aeropuertos
        ]
    )


@data_bp.route("/movimientos", methods=["GET"])
def get_movimientos():
    """
    Retrieve a list of all movimientos (flight movements, e.g., arrivals, departures) from the database, including their IDs and descriptions.

    Returns:
        A JSON list of all flight movements, each represented by a dictionary containing the movement's ID and description.
    """
    all_movimientos = Movimientos.query.all()
    return jsonify(
        [
            {"id": movimiento.id_movimiento, "descripcion": movimiento.descripcion}
            for movimiento in all_movimientos
        ]
    )


@data_bp.route("/vuelos", methods=["GET"])
def get_vuelos():
    """
    Retrieve a list of all vuelos (flights) from the database, including detailed information.

    Returns:
        A JSON list of flights, each with detailed information including the flight ID, the airline name,
        the airport name, the type of movement, and the date of the flight.
    """
    all_vuelos = Vuelos.query.all()
    vuelos_data = [
        {
            "id_vuelo": vuelo.id_vuelo,
            "nombre_aerolinea": Aerolineas.query.filter_by(
                id_aerolinea=vuelo.id_aerolinea
            )
            .first()
            .nombre_aerolinea,
            "nombre_aeropuerto": Aeropuertos.query.filter_by(
                id_aeropuerto=vuelo.id_aeropuerto
            )
            .first()
            .nombre_aeropuerto,
            "tipo_movimiento": Movimientos.query.filter_by(
                id_movimiento=vuelo.id_movimiento
            )
            .first()
            .descripcion,
            "dia": vuelo.dia.strftime("%Y-%m-%d"),
        }
        for vuelo in all_vuelos
    ]
    return jsonify(vuelos_data)
