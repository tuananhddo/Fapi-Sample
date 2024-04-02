from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.exceptions.exceptions import CustomException, DuplicateData
import string


async def duplicate_exception_handler(request, exc: DuplicateData):
    # return PlainTextResponse("validation handler", status_code=400)
    mss = exc.message
    mss_tmp = exc.message_template
    field = exc.identity_field

    if mss_tmp and string.Template(mss):
        final_mss = mss_tmp.format(field)
    else:
        final_mss = mss
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "detail": {
                "field": exc.identity_field,
                "message": final_mss
            }, 
        }),
    )

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
    return PlainTextResponse(f"HTTP {str(exc.detail)}", status_code=exc.status_code)

async def unicorn_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )