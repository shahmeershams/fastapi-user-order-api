# app/services/auth_service.py

from sqlalchemy.orm import Session
from app.database.models import User, AuthenticateToken, Role
from app.validators import UserLogin, TokenResponse, UserResponse
from app.utils import verify_password, create_access_token, create_refresh_token, verify_token
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError
import os

class AuthService:
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """Authenticate user by username/email and password"""
        # Check if username is email or username
        user = db.query(User).filter(
            (User.email == username) | (User.username == username)
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        return user
    
    @staticmethod
    def create_tokens(db: Session, user: User) -> TokenResponse:
        """Create access and refresh tokens for user"""
        # Load user role for JWT claims
        user_with_role = db.query(User).join(Role).filter(User.user_id == user.user_id).first()
        
        # JWT payload with user info and role
        token_data = {
            "sub": str(user.user_id),
            "username": user.username,
            "email": user.email,
            "role": user_with_role.role.key,
            "role_id": user.role_id
        }
        
        # Create tokens with different expiry times
        ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
        
        access_token = create_access_token(
            data=token_data,
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        refresh_token = create_refresh_token(
            data={"sub": str(user.user_id)},
            expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
        
        # Calculate expiry times
        access_expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        # Store tokens in database
        auth_token = AuthenticateToken(
            user_id=user.user_id,
            access_token=access_token,
            access_token_expires_at=access_expires_at,
            refresh_token=refresh_token,
            refresh_token_expires_at=refresh_expires_at
        )
        
        db.add(auth_token)
        db.commit()
        db.refresh(auth_token)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user_with_role)
        )
    
    @staticmethod
    def login(db: Session, credentials: UserLogin) -> TokenResponse:
        """Login user and return tokens"""
        # Authenticate user
        user = AuthService.authenticate_user(db, credentials.username, credentials.password)
        
        # Invalidate existing tokens for this user (optional - single session)
        # db.query(AuthenticateToken).filter_by(user_id=user.user_id).delete()
        
        # Create new tokens
        return AuthService.create_tokens(db, user)
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token"""
        try:
            # Verify refresh token
            payload = verify_token(refresh_token)
            user_id = int(payload.get("sub"))
            
            # Check if it's a refresh token
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type"
                )
            
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Get token from database
        db_token = db.query(AuthenticateToken).filter(
            AuthenticateToken.refresh_token == refresh_token,
            AuthenticateToken.user_id == user_id
        ).first()
        
        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token not found or expired"
            )
        
        # Check if refresh token is expired
        if datetime.utcnow() > db_token.refresh_token_expires_at:
            # Clean up expired token
            db.delete(db_token)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
        
        # Get user
        user = db.query(User).filter_by(user_id=user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create new tokens
        new_tokens = AuthService.create_tokens(db, user)
        
        # Delete old token record
        db.delete(db_token)
        db.commit()
        
        return new_tokens
    
    @staticmethod
    def get_current_user_from_token(db: Session, token: str) -> User:
        """Get current user from access token"""
        try:
            payload = verify_token(token)
            user_id = int(payload.get("sub"))
            
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload"
                )
            
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Get user with role information
        user = db.query(User).join(Role).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
    
    @staticmethod
    def logout(db: Session, user_id: int):
        """Logout user by invalidating all tokens"""
        db.query(AuthenticateToken).filter_by(user_id=user_id).delete()
        db.commit()
    
    @staticmethod
    def cleanup_expired_tokens(db: Session):
        """Clean up expired tokens from database"""
        now = datetime.utcnow()
        expired_tokens = db.query(AuthenticateToken).filter(
            (AuthenticateToken.access_token_expires_at < now) &
            (AuthenticateToken.refresh_token_expires_at < now)
        )
        expired_count = expired_tokens.count()
        expired_tokens.delete()
        db.commit()
        return expired_count
