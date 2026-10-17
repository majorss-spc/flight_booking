
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        email = str(user.email).strip().lower()

        existing_user = UserRepository.get_by_email(db, email)
        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already exists",
            )

        # UserCreate contains no password or role fields.
        user_data = user.model_copy(update={"email": email})
        return UserRepository.create(db, user_data)

    @staticmethod
    def get_all_users(db: Session):
        return UserRepository.get_all(db)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        return user

    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        user_data: UserUpdate,
    ):
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        updates = user_data.model_dump(exclude_unset=True)

        if "email" in updates:
            if updates["email"] is None:
                raise HTTPException(
                    status_code=422,
                    detail="Email cannot be null",
                )

            email = str(updates["email"]).strip().lower()
            existing_user = UserRepository.get_by_email(db, email)

            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=409,
                    detail="Email already exists",
                )

            updates["email"] = email

        # Only fields allowed by UserUpdate are changed.
        safe_data = UserUpdate(**updates)
        return UserRepository.update(db, user, safe_data)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        UserRepository.delete(db, user)

        return {"message": "User deleted successfully"}
