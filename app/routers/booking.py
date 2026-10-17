
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse
from app.services import booking_service as service


router = APIRouter(prefix="/bookings", tags=["Bookings"])


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


# Create booking: logged-in user only
@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create_booking(
        db=db,
        booking_data=booking_data,
        user_id=current_user.id,
    )


# View all bookings: admin only
@router.get("/", response_model=list[BookingResponse])
def get_all_bookings(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return service.get_all_bookings(db)


# View a booking: owner or admin
@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = service.get_booking(db, booking_id)

    if current_user.role != "ADMIN" and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own bookings",
        )

    return booking


# View bookings for a user: owner or admin
@router.get("/user/{user_id}", response_model=list[BookingResponse])
def get_user_bookings(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "ADMIN" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own bookings",
        )

    return service.get_user_bookings(db, user_id)


# Cancel a booking: owner or admin
@router.delete("/{booking_id}", response_model=BookingResponse)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = service.get_booking(db, booking_id)

    if current_user.role != "ADMIN" and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only cancel your own bookings",
        )

    return service.cancel_booking(db, booking_id)
