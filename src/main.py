import os
import types

from src.core.openapi import custom_openapi
from src.exceptions.exception_handler import (
    duplicate_exception_handler, general_handler, http_exception_handler, 
    unicorn_exception_handler, validation_exception_handler
)
from src.exceptions.exceptions import CustomException, DuplicateData
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.database import create_db_and_tables, reset_database
from .routers.users import router as su_router
from .routers.auth import router as auth_router
from .routers.health import router as health_router

app = FastAPI()


# @app.on_event("startup")
# def on_startup():
    # reset_database()
    # create_db_and_tables()
# Example usage:
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.origins,
#     allow_credentials=True,
#     allow_methods=["*"],
# )
app.openapi = types.MethodType(custom_openapi, app)

app.add_exception_handler(DuplicateData, duplicate_exception_handler)
app.add_exception_handler(CustomException, unicorn_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_handler)

app.include_router(su_router)
app.include_router(auth_router)
app.include_router(health_router)









