
from sqlalchemy.orm import Session

from app.models.booking import Booking


def create(db: Session, booking: Booking):
    db.add(booking)
    db.flush()
    return booking


def get_all(db: Session):
    return db.query(Booking).all()


def get_by_id(db: Session, booking_id: int):
    return (
        db.query(Booking)
        .filter(Booking.id == booking_id)
        .first()
    )


def get_by_user_id(db: Session, user_id: int):
    return (
        db.query(Booking)
        .filter(Booking.user_id == user_id)
        .all()
    )


def update(db: Session, booking: Booking, updates: dict):
    for key, value in updates.items():
        setattr(booking, key, value)

    db.flush()
    return booking


def delete(db: Session, booking: Booking):
    db.delete(booking)
    db.flush()
