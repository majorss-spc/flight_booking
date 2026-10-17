
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import flight_repository as repo
from app.schemas.flight import FlightCreate, FlightUpdate


def create_flight(db: Session, flight: FlightCreate):
    if flight.origin.strip().casefold() == flight.destination.strip().casefold():
        raise HTTPException(
            status_code=400,
            detail="Origin and destination cannot be the same",
        )

    if flight.arrival_time <= flight.departure_time:
        raise HTTPException(
            status_code=400,
            detail="Arrival time must be after departure time",
        )

    existing = repo.get_by_flight_number(db, flight.flight_number.strip())
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Flight number already exists",
        )

    flight_data = flight.model_copy(
        update={"flight_number": flight.flight_number.strip()}
    )
    return repo.create(db, flight_data)


def get_all_flights(db: Session):
    return repo.get_all(db)


def get_flight(db: Session, flight_id: int):
    flight = repo.get_by_id(db, flight_id)

    if not flight:
        raise HTTPException(
            status_code=404,
            detail="Flight not found",
        )

    return flight


def update_flight(
    db: Session,
    flight_id: int,
    flight_data: FlightUpdate,
):
    flight = get_flight(db, flight_id)
    updates = flight_data.model_dump(exclude_unset=True)

    new_origin = updates.get("origin", flight.origin)
    new_destination = updates.get("destination", flight.destination)

    if (
        new_origin is not None
        and new_destination is not None
        and new_origin.strip().casefold() == new_destination.strip().casefold()
    ):
        raise HTTPException(
            status_code=400,
            detail="Origin and destination cannot be the same",
        )

    new_departure = updates.get("departure_time", flight.departure_time)
    new_arrival = updates.get("arrival_time", flight.arrival_time)

    if new_departure is not None and new_arrival is not None:
        if new_arrival <= new_departure:
            raise HTTPException(
                status_code=400,
                detail="Arrival time must be after departure time",
            )

    if "flight_number" in updates and updates["flight_number"] is not None:
        flight_number = updates["flight_number"].strip()
        existing = repo.get_by_flight_number(db, flight_number)

        if existing and existing.id != flight_id:
            raise HTTPException(
                status_code=409,
                detail="Flight number already exists",
            )

        updates["flight_number"] = flight_number

    safe_data = FlightUpdate(**updates)
    return repo.update(db, flight, safe_data)


def delete_flight(db: Session, flight_id: int):
    flight = get_flight(db, flight_id)

    # Prevent deleting a flight that has booking records.
    from app.models.booking import Booking

    existing_booking = (
        db.query(Booking)
        .filter(Booking.flight_id == flight_id)
        .first()
    )

    if existing_booking:
        raise HTTPException(
            status_code=409,
            detail="Flight has booking records and cannot be deleted",
        )

    repo.delete(db, flight)
    return {"message": "Flight deleted successfully"}
