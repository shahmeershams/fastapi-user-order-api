# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services import UserService
from app.validators import UserCreate, UserUpdate, UserResponse, UserListResponse
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    return UserService.create_user(db, user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    return UserService.get_user(db, user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Update user by ID"""
    return UserService.update_user(db, user_id, user_update)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete user by ID"""
    UserService.delete_user(db, user_id)
    return None

@router.get("/", response_model=UserListResponse)
def list_users(page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
    """List all users with pagination"""
    return UserService.list_users(db, page, per_page)
