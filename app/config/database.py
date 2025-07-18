# app/config/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv

# Load the environment variables from .env
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost/dbname")
echo_sql = False

# Create the SQLAlchemy engine with MySQL settings
engine = create_engine(DATABASE_URL, echo=echo_sql)

# Create a session class that will be used to interact with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """
    Database dependency function
    
    This function creates a database session and yields it to the caller.
    It ensures the session is properly closed after use.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
