# app/models/user.py

from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from app.database.session import Base

class User(Base):
    __tablename__ = "users"  # This will be the table name in PostgreSQL

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="customer")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
