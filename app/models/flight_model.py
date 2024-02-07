from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Aerolineas(db.Model):
    """
    Model for the Aerolineas table.
    Represents airlines with an ID and name.

    Attributes:
        id_aerolinea (db.Integer): The primary key, unique ID for the airline.
        nombre_aerolinea (db.String): The name of the airline.
    """

    id_aerolinea = db.Column(db.Integer, primary_key=True)
    nombre_aerolinea = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        """
        Provides a string representation of an Aerolineas instance, showcasing the airline's name.

        Returns:
            str: A string representation of the airline.
        """
        return f"<Aerolineas {self.nombre_aerolinea}>"


class Aeropuertos(db.Model):
    """
    Model for the Aeropuertos table.
    Represents airports with an ID and name.
    """

    id_aeropuerto = db.Column(db.Integer, primary_key=True)
    nombre_aeropuerto = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Aeropuertos {self.nombre_aeropuerto}>"


class Movimientos(db.Model):
    """
    Model for the Movimientos table.
    Represents flight movements (e.g., arrivals, departures) with an ID and description.
    """

    id_movimiento = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Movimientos {self.descripcion}>"


class Vuelos(db.Model):
    """
    Model for the Vuelos table.
    Represents flights with an auto-incrementing ID, links to airlines (Aerolineas),
    airports (Aeropuertos), movements (Movimientos), and a date.
    """

    id_vuelo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aerolinea = db.Column(
        db.Integer, db.ForeignKey("aerolineas.id_aerolinea"), nullable=False
    )
    id_aeropuerto = db.Column(
        db.Integer, db.ForeignKey("aeropuertos.id_aeropuerto"), nullable=False
    )
    id_movimiento = db.Column(
        db.Integer, db.ForeignKey("movimientos.id_movimiento"), nullable=False
    )
    dia = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Vuelos {self.id_vuelo}>"
