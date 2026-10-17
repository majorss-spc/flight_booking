
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


# Flight create karne ke liye request schema
class FlightCreate(BaseModel):
    airline: str = Field(min_length=2, max_length=100)
    flight_number: str = Field(min_length=2, max_length=20)
    origin: str = Field(min_length=2, max_length=100)
    destination: str = Field(min_length=2, max_length=100)
    departure_time: datetime
    arrival_time: datetime
    price: float = Field(gt=0)
    available_seats: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_flight_details(self):
        if self.origin.strip().casefold() == self.destination.strip().casefold():
            raise ValueError("Origin and destination cannot be the same")

        if self.arrival_time <= self.departure_time:
            raise ValueError("Arrival time must be after departure time")

        return self


# Flight update karne ke liye request schema
class FlightUpdate(BaseModel):
    airline: str | None = Field(default=None, min_length=2, max_length=100)
    flight_number: str | None = Field(default=None, min_length=2, max_length=20)
    origin: str | None = Field(default=None, min_length=2, max_length=100)
    destination: str | None = Field(default=None, min_length=2, max_length=100)
    departure_time: datetime | None = None
    arrival_time: datetime | None = None
    price: float | None = Field(default=None, gt=0)
    available_seats: int | None = Field(default=None, ge=0)


# API response schema
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
