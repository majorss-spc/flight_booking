from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class FlightCreate(BaseModel):
    airline: str
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price: float = Field(gt=0)
    available_seats: int = Field(ge=0)


class FlightUpdate(BaseModel):
    airline: str | None = None
    flight_number: str | None = None
    origin: str | None = None
    destination: str | None = None
    departure_time: datetime | None = None
    arrival_time: datetime | None = None
    price: float | None = Field(default=None, gt=0)
    available_seats: int | None = Field(default=None, ge=0)


class FlightResponse(BaseModel):
    id: int
    airline: str
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    available_seats: int

    model_config = ConfigDict(from_attributes=True)
