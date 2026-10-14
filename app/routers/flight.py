from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.flight import FlightCreate, FlightUpdate, FlightResponse
from app.services import flight_service as service

router = APIRouter(prefix="/flights", tags=["Flights"])


@router.post("/", response_model=FlightResponse, status_code=status.HTTP_201_CREATED)
def create_flight(flight: FlightCreate, db: Session = Depends(get_db)):
    return service.create_flight(db, flight)


@router.get("/", response_model=list[FlightResponse])
def get_all_flights(db: Session = Depends(get_db)):
    return service.get_all_flights(db)


@router.get("/{flight_id}", response_model=FlightResponse)
def get_flight(flight_id: int, db: Session = Depends(get_db)):
    return service.get_flight(db, flight_id)


@router.put("/{flight_id}", response_model=FlightResponse)
def update_flight(
    flight_id: int,
    flight_data: FlightUpdate,
    db: Session = Depends(get_db)
):
    return service.update_flight(db, flight_id, flight_data)


@router.delete("/{flight_id}")
def delete_flight(flight_id: int, db: Session = Depends(get_db)):
    return service.delete_flight(db, flight_id)
