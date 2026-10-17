
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Load database and JWT configuration from .env
class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

# Connect SQLAlchemy to MySQL
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

# Create database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for all database models
Base = declarative_base()


# Provide a database session to each API request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
