# app/routers/ping.py

from fastapi import APIRouter

# Create a router instance
router = APIRouter()

# Define a GET endpoint at /ping
@router.get("/ping")
def ping():
    return {"message": "pong"}
