from fastapi import FastAPI

from src.settings import settings
from .routers.sample_users import router as su_router
# from .routers import users


# from .database import SessionLocal, engine
# from .models import base as models
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.include_router(users.router)
app.include_router(su_router)

@app.get("/ping")
async def root():
    return {"message": "Pong"}

@app.get("/env")
async def envs():
    return {"message": settings}