# main.py

from fastapi import FastAPI
from app.routers import ping
# from app.database.models import user, order  
# from app.config.database import SessionLocal, engine  

app = FastAPI()

# Register router immediately after app is created
app.include_router(ping.router)



