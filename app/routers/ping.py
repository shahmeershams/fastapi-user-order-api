from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root_check():
    return {"message": "API is running!"}

@router.get("/ping")
def ping():
    return {"message": "pong"}
