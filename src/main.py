from fastapi import FastAPI
from .routers.users import router as urouter
# from .routers import users
app = FastAPI()

# app.include_router(users.router)
app.include_router(urouter)

@app.get("/")
async def root():
    return {"message": "Hello World"}