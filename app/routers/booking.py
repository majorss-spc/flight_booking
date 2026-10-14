from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse
from app.services import booking_service as service

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db)
):
    return service.create_booking(db, booking_data)


@router.get("/", response_model=list[BookingResponse])
def get_all_bookings(db: Session = Depends(get_db)):
    return service.get_all_bookings(db)


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    return service.get_booking(db, booking_id)


@router.get("/user/{user_id}", response_model=list[BookingResponse])
def get_user_bookings(
    user_id: int,
    db: Session = Depends(get_db)
):
    return service.get_user_bookings(db, user_id)


@router.delete("/{booking_id}", response_model=BookingResponse)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    return service.cancel_booking(db, booking_id)
