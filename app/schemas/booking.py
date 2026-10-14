from pydantic import BaseModel, ConfigDict, Field


class BookingCreate(BaseModel):
    user_id: int = Field(gt=0)
    flight_id: int = Field(gt=0)
    number_of_seats: int = Field(gt=0)


class BookingUpdate(BaseModel):
    number_of_seats: int | None = Field(default=None, gt=0)


class BookingResponse(BaseModel):
    id: int
    user_id: int
    flight_id: int
    number_of_seats: int
    total_price: float
    booking_status: str

    model_config = ConfigDict(from_attributes=True)
