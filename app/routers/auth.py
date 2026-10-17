
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.database import get_db
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse


# Auth ki saari APIs /auth prefix ke andar hongi.
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    # Check karo ki email pehle se registered toh nahi.
    existing_user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    # Plain password ko hash karo; original password save mat karo.
    user = User(
        name=request.name,
        email=str(request.email),
        phone=request.phone,
        password_hash=hash_password(request.password),
        role="USER",
    )

    # User ko database mein save karo.
    db.add(user)
    db.commit()
    db.refresh(user)

    # Naye user ke liye JWT token banao.
    token = create_access_token(
        user_id=user.id,
        role=user.role,
    )

    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login_user(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    # Email se user find karo.
    user = (
        db.query(User)
        .filter(User.email == str(request.email))
        .first()
    )

    # User na mile ya password hash missing ho toh login reject karo.
    if (
        user is None
        or user.password_hash is None
        or not verify_password(request.password, user.password_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Valid credentials par JWT generate karo.
    token = create_access_token(
        user_id=user.id,
        role=user.role,
    )

    return TokenResponse(access_token=token)
