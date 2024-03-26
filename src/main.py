import os
import src.log_config

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from src.settings import settings
from .routers.users import router as su_router
from .routers.auth import router as auth_router
from .routers.health import router as health_router

# from .routers import users

app = FastAPI()


# app.include_router(users.router)
app.include_router(su_router)
app.include_router(auth_router)
app.include_router(health_router)

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder
# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# @app.exception_handler(RequestValidationError)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc), status_code=400)


# Example usage:
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.origins,
#     allow_credentials=True,
#     allow_methods=["*"],
# )


# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(        
#         title="Custom Title",
#         version="1.0.0",
#         description="Custom Description",
#         routes=app.routes,)
#     if "securitySchemes" not in openapi_schema['components']:
#         openapi_schema['components'].update({
#             "securitySchemes": {
#                     "CustomSecurityScheme": {
#                     'type': 'apiKey',
#                     'in': 'header',
#                     'name': 'MyCustomHeader'
#                 }
#             }
#         })
        
#         for pkey, path in openapi_schema['paths'].items():
#             for pm_key, path_m_data in path.items():
#                 sec_list = [{
#                     "CustomSecurityScheme": []
#                 }]
#                 if 'security' in path_m_data:
#                     path_m_data['security'] += sec_list
#                 else:
#                     path_m_data['security'] = sec_list
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# # Assign the custom_openapi function to the app.openapi attribute
# app.openapi = custom_openapi


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     print("CMD")
#     return PlainTextResponse("CMD", status_code=400)

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

