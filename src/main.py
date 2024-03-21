from typing import Annotated
from fastapi import Depends, FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.models import ( 
    Response as OpenAPIResponse, 
    Reference
)
from src.settings import settings
from src.utils.auth import get_password_hash
from .routers.sample_users import router as su_router
from .routers.auth import router as auth_router
# from .routers import users
from fastapi.openapi.models import SecurityBase


# from .database import SessionLocal, engine
# from .models import base as models
# models.Base.metadata.create_all(bind=engine)
def dps():
    return SecurityBase(
        type="apiKey",
        in_="header",
        name="Authorizationz"
    )
app = FastAPI()

# app.include_router(users.router)
app.include_router(su_router)
app.include_router(auth_router)


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom Title",
        version="1.0.0",
        description="Custom Description",
        routes=app.routes,
    )
    # # Add global headers to OpenAPI responses
    # for response_name, response in openapi_schema["components"]["responses"].items():
    #     response_model = response.get("content", {}).get("application/json", {}).get("schema")
    #     if response_model and isinstance(response_model, Reference):
    #         response_model = openapi_schema["components"]["schemas"][response_model["$ref"].split("/")[-1]]
    #     if response_model and isinstance(response_model, OpenAPIResponse):
    #         if "headers" not in response_model:
    #             response_model["headers"] = {}
    #         response_model["headers"].update(GLOBAL_HEADERS)

    # openapi_schema["components"]["headers"] = {
    #     "Authorizationz": {
    #         "description": "HDS",
    #         "required": "true",
    #         "schema": {
    #             "type": "string"
    #         }
    #     }
    # }
    # openapi_schema["info"]["title"] = "XYZ"
    # openapi_schema['security'] = [dps()]

    openapi_schema['components']["securitySchemes"]["SomeKind"] = {
            'type': 'apiKey',
            'in': 'header',
            'name': 'aaaaaa'
        }
    
    for pkey, path in openapi_schema['paths'].items():
        for pm_key, path_m_data in path.items():
            sec_list = [{
                "Authorizationz": []
            }]
            if 'security' in path_m_data:
                path_m_data['security'] += sec_list
            else:
                path_m_data['security'] = sec_list
        print(1)
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Assign the custom_openapi function to the app.openapi attribute
app.openapi = custom_openapi
# app.openapi = {
#     "info": {
#         "title": "Your API",
#         "version": "1.0",
#         "description": "Your API description"
#     },
#     "security": [dps()]
# }
@app.get("/ping")
async def root():
    return {"message": "Pong"}

@app.get("/env")
async def envs(user_agent: Annotated[str | None, Header()]):
    print(get_password_hash("test"))
    return {"message": settings}