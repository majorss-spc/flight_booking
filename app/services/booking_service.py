from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.flight import Flight
from app.models.booking import Booking
from app.repositories import booking_repository as repo
from app.schemas.booking import BookingCreate


def create_booking(db: Session, booking_data: BookingCreate):
    user = db.query(User).filter(
        User.id == booking_data.user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    flight = db.query(Flight).filter(
        Flight.id == booking_data.flight_id
    ).with_for_update().first()

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    if booking_data.number_of_seats > flight.available_seats:
        raise HTTPException(status_code=400, detail="Not enough available seats")

    total_price = flight.price * booking_data.number_of_seats
    flight.available_seats -= booking_data.number_of_seats

    booking = Booking(
        user_id=booking_data.user_id,
        flight_id=booking_data.flight_id,
        number_of_seats=booking_data.number_of_seats,
        total_price=total_price,
        booking_status="confirmed"
    )

    try:
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking
    except Exception:
        db.rollback()
        raise


def get_all_bookings(db: Session):
    return repo.get_all(db)


def get_booking(db: Session, booking_id: int):
    booking = repo.get_by_id(db, booking_id)

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking


def get_user_bookings(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return repo.get_by_user_id(db, user_id)


def cancel_booking(db: Session, booking_id: int):
    booking = get_booking(db, booking_id)

    if booking.booking_status == "cancelled":
        raise HTTPException(status_code=400, detail="Booking is already cancelled")

    flight = db.query(Flight).filter(
        Flight.id == booking.flight_id
    ).with_for_update().first()

    if flight:
        flight.available_seats += booking.number_of_seats

    booking.booking_status = "cancelled"

    try:
        db.commit()
        db.refresh(booking)
        return booking
    except Exception:
        db.rollback()
        raise
