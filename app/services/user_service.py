
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        existing_user = UserRepository.get_by_email(
            db, str(user.email)
        )

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

        return UserRepository.create(db, user)

    @staticmethod
    def get_all_users(db: Session):
        return UserRepository.get_all(db)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        user_data: UserUpdate
    ):
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        update_data = user_data.model_dump(exclude_unset=True)

        if "email" in update_data and update_data["email"] is not None:
            existing_user = UserRepository.get_by_email(
                db, str(update_data["email"])
            )

            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=409,
                    detail="Email already exists"
                )

        return UserRepository.update(db, user, user_data)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        UserRepository.delete(db, user)

        return {"message": "User deleted successfully"}
