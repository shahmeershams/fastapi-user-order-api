# app/services/user_service.py

from sqlalchemy.orm import Session
from app.database.models import User, Role
from app.validators import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.utils import hash_password
from fastapi import HTTPException, status

class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> UserResponse:
        # Check for existing user
        existing_user = db.query(User).filter_by(email=user.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
        # Get role_id - either provided or default to customer role
        role_id = user.role_id
        if not role_id:
            # Look up customer role dynamically
            customer_role = db.query(Role).filter_by(key="customer").first()
            if not customer_role:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Default customer role not found. Please contact administrator."
                )
            role_id = customer_role.role_id
        
        # Validate that the role exists
        role = db.query(Role).filter_by(role_id=role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role with ID {role_id} not found"
            )
        
        # Create new user
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
            role_id=role_id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserResponse.model_validate(new_user)

    @staticmethod
    def get_user(db: Session, user_id: int) -> UserResponse:
        user = db.query(User).filter_by(user_id=user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user)

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> UserResponse:
        user = db.query(User).filter_by(user_id=user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Update fields
        if user_update.username:
            user.username = user_update.username
        if user_update.email:
            user.email = user_update.email
        if user_update.password:
            user.hashed_password = hash_password(user_update.password)
        
        db.commit()
        db.refresh(user)
        return UserResponse.model_validate(user)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(User).filter_by(user_id=user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db.delete(user)
        db.commit()
        
    @staticmethod
    def list_users(db: Session, page: int = 1, per_page: int = 10) -> UserListResponse:
        query = db.query(User)
        total = query.count()
        users = query.offset((page - 1) * per_page).limit(per_page).all()
        return UserListResponse(users=[UserResponse.model_validate(user) for user in users], total=total, page=page, per_page=per_page)

