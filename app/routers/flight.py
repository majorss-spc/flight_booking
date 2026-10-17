
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.flight import FlightCreate, FlightUpdate, FlightResponse
from app.services import flight_service as service


router = APIRouter(prefix="/flights", tags=["Flights"])


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


# Create flight: admin only
@router.post(
    "/",
    response_model=FlightResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_flight(
    flight: FlightCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return service.create_flight(db, flight)


# Search all flights: public
@router.get("/", response_model=list[FlightResponse])
def get_all_flights(db: Session = Depends(get_db)):
    return service.get_all_flights(db)


# Get one flight: public
@router.get("/{flight_id}", response_model=FlightResponse)
def get_flight(
    flight_id: int,
    db: Session = Depends(get_db),
):
    return service.get_flight(db, flight_id)


# Update flight: admin only
@router.put("/{flight_id}", response_model=FlightResponse)
def update_flight(
    flight_id: int,
    flight_data: FlightUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return service.update_flight(db, flight_id, flight_data)


# Delete flight: admin only
@router.delete("/{flight_id}")
def delete_flight(
    flight_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return service.delete_flight(db, flight_id)
