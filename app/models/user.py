
from sqlalchemy import Column, Integer, String
from app.database import Base


class User(Base):
    __tablename__ = "users"

    # Unique ID for every user
    id = Column(Integer, primary_key=True, index=True)

    # Basic user details
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)

    # Hashed password; NULL temporarily allowed for existing accounts
    password_hash = Column(String(255), nullable=True)

    # Every new user gets USER role by default
    role = Column(String(20), nullable=False, default="USER")
