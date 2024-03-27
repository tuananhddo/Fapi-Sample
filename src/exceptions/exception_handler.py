from fastapi.exception_handlers import (
    request_validation_exception_handler
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder

from src.exceptions.exceptions import CustomException

async def validation_exception_handler(request, exc):
    # return PlainTextResponse("validation handler", status_code=400)
    print("Do Anything Here. E.g i18n")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

async def general_handler(request, exc):
    return PlainTextResponse("general_handler", status_code=400)

async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

async def unicorn_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )