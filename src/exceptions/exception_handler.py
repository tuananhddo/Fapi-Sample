from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder
from main import app



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print("XYZZZ")
    return PlainTextResponse("TAOsKCDD", status_code=400)