from fastapi import FastAPI
from .routers.users import router as urouter
# from .routers import users


# from .database import SessionLocal, engine
# from .models import base as models
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.include_router(users.router)
app.include_router(urouter)

@app.get("/")
async def root():
    return {"message": "Hello World"}