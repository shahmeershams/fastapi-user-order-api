# app/config/database.py

# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base, Session
# from dotenv import load_dotenv

# # Load the environment variables from .env
# load_dotenv()

# # Read the database URL from .env
# DATABASE_URL = os.getenv("DATABASE_URL")

# # Create the SQLAlchemy engine
# engine = create_engine(DATABASE_URL)

# # Create a session class that will be used to interact with the DB
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base class for models
# Base = declarative_base()

# def get_db():
#     db: Session = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
