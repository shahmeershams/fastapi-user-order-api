# app/config/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv

# Load the environment variables from .env
load_dotenv()

# Get environment type
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Environment-based database configuration
if ENVIRONMENT == "testing":
    # Use SQLite in-memory database for testing
    DATABASE_URL = "sqlite:///:memory:"
    echo_sql = True
elif ENVIRONMENT == "development":
    # Use PostgreSQL for development
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:secret123@localhost:5432/orders_db")
    echo_sql = False
else:
    # Production
    DATABASE_URL = os.getenv("DATABASE_URL")
    echo_sql = False

print(f"🔧 Environment: {ENVIRONMENT}")
print(f"🗄️  Database: {DATABASE_URL.split('://')[0]}")

# Create the SQLAlchemy engine with appropriate settings
if DATABASE_URL.startswith("sqlite"):
    # SQLite specific settings
    engine = create_engine(
        DATABASE_URL,
        echo=echo_sql,
        connect_args={"check_same_thread": False}  # Needed for SQLite with FastAPI
    )
else:
    # PostgreSQL settings
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
