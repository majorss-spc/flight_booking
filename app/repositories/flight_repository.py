from sqlalchemy.orm import Session
from app.models.flight import Flight
from app.schemas.flight import FlightCreate, FlightUpdate


def create(db: Session, flight: FlightCreate):
    db_flight = Flight(**flight.model_dump())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight


def get_all(db: Session):
    return db.query(Flight).all()


def get_by_id(db: Session, flight_id: int):
    return db.query(Flight).filter(Flight.id == flight_id).first()


def get_by_flight_number(db: Session, flight_number: str):
    return db.query(Flight).filter(
        Flight.flight_number == flight_number
    ).first()


def update(db: Session, db_flight: Flight, flight_data: FlightUpdate):
    for key, value in flight_data.model_dump(exclude_unset=True).items():
        setattr(db_flight, key, value)

    db.commit()
    db.refresh(db_flight)
    return db_flight


def delete(db: Session, db_flight: Flight):
    db.delete(db_flight)
    db.commit()
