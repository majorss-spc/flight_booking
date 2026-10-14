from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import flight_repository as repo
from app.schemas.flight import FlightCreate, FlightUpdate


def create_flight(db: Session, flight: FlightCreate):
    existing = repo.get_by_flight_number(db, flight.flight_number)

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Flight number already exists"
        )

    if flight.arrival_time <= flight.departure_time:
        raise HTTPException(
            status_code=400,
            detail="Arrival time must be after departure time"
        )

    return repo.create(db, flight)


def get_all_flights(db: Session):
    return repo.get_all(db)


def get_flight(db: Session, flight_id: int):
    flight = repo.get_by_id(db, flight_id)

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    return flight


def update_flight(db: Session, flight_id: int, flight_data: FlightUpdate):
    flight = get_flight(db, flight_id)
    updates = flight_data.model_dump(exclude_unset=True)

    new_flight_number = updates.get("flight_number")
    if new_flight_number and new_flight_number != flight.flight_number:
        existing = repo.get_by_flight_number(db, new_flight_number)
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Flight number already exists"
            )

    departure = updates.get("departure_time", flight.departure_time)
    arrival = updates.get("arrival_time", flight.arrival_time)

    if arrival <= departure:
        raise HTTPException(
            status_code=400,
            detail="Arrival time must be after departure time"
        )

    return repo.update(db, flight, flight_data)


def delete_flight(db: Session, flight_id: int):
    flight = get_flight(db, flight_id)
    repo.delete(db, flight)
    return {"message": "Flight deleted successfully"}
