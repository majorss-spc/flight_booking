from fastapi import FastAPI
from app.routers import auth
from app.database import Base, engine
from app.models.user import User
from app.models.flight import Flight
from app.models.booking import Booking

from app.routers.user import router as user_router
from app.routers.flight import router as flight_router
from app.routers.booking import router as booking_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flight Booking API")

app.include_router(auth.router)
app.include_router(user_router)
app.include_router(flight_router)
app.include_router(booking_router)


@app.get("/")
def home():
    return {"message": "Flight Booking API is running"}
