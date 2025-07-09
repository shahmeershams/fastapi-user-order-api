# app/main.py
# Initial setup by Shahmeer Ahmad Bhatti

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal, engine
from app.models import user, order  #  import models so SQLAlchemy sees them
from app.routers import ping  #  new router for /ping

# Create the tables in the DB (only runs once)
user.Base.metadata.create_all(bind=engine)
order.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB dependency for root check
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root route - tests DB connection
@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"message": "Connected to the database!"}

# Ping route - tests API connection
app.include_router(ping.router)
