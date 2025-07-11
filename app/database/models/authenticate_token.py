# app/database/models/authenticate_token.py

from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.config.database import Base

class AuthenticateToken(Base):
    """
    Authentication Token Model
    
    This model stores JWT tokens for user authentication.
    It manages both access tokens (short-lived) and refresh tokens (long-lived)
    for secure user sessions.
    """
    __tablename__ = "authenticate_tokens"

    token_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    access_token = Column(Text, nullable=False)  # JWT access token
    access_token_expires_at = Column(TIMESTAMP, nullable=False)
    refresh_token = Column(Text, nullable=False)  # JWT refresh token
    refresh_token_expires_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="authenticate_tokens")

    def __repr__(self):
        return f"<AuthenticateToken(token_id={self.token_id}, user_id={self.user_id})>"
