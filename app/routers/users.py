# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services import UserService
from app.validators import UserCreate, UserUpdate, UserResponse, UserListResponse, CurrentUserResponse
from app.dependencies import (
    get_current_active_user, require_admin, require_permission, 
    check_resource_ownership, get_current_user_id
)
from app.database.models import User
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create a new user (Admin only).
    
    Only administrators can create new users.
    """
    return UserService.create_user(db, user)

@router.get("/me", response_model=CurrentUserResponse, response_model_exclude_none=True)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's own profile.
    
    Returns the profile of the currently authenticated user.
    """
    # Convert to CurrentUserResponse which may include additional fields
    return CurrentUserResponse.model_validate(current_user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get user by ID.
    
    - Admins can view any user
    - Customers can only view their own profile
    """
    # Check if user can access this resource
    if current_user.role.key != "admin" and current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only view your own profile."
        )
    
    return UserService.get_user(db, user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update user by ID.
    
    - Admins can update any user
    - Customers can only update their own profile
    """
    # Check if user can access this resource
    if current_user.role.key != "admin" and current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only update your own profile."
        )
    
    return UserService.update_user(db, user_id, user_update)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete user by ID (Admin only).
    
    Only administrators can delete users.
    """
    # Prevent admin from deleting themselves
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete your own account through this endpoint."
        )
    
    UserService.delete_user(db, user_id)
    return None

@router.get("/", response_model=UserListResponse)
def list_users(
    page: int = 1, 
    per_page: int = 10, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    List all users with pagination (Admin only).
    
    Only administrators can view the list of all users.
    """
    return UserService.list_users(db, page, per_page)

