from typing import Annotated
from fastapi import Depends, FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from src.settings import settings
from src.utils.auth import get_password_hash
from .routers.sample_users import router as su_router
from .routers.auth import router as auth_router
# from .routers import users

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
        routes=app.routes,)

    openapi_schema['components']["securitySchemes"]["CustomSecurityScheme"] = {
            'type': 'apiKey',
            'in': 'header',
            'name': 'MyCustomHeader'
        }
    
    for pkey, path in openapi_schema['paths'].items():
        for pm_key, path_m_data in path.items():
            sec_list = [{
                "CustomSecurityScheme": []
            }]
            if 'security' in path_m_data:
                path_m_data['security'] += sec_list
            else:
                path_m_data['security'] = sec_list
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Assign the custom_openapi function to the app.openapi attribute
app.openapi = custom_openapi

@app.get("/ping")
async def root():
    return {"message": "Pong"}

@app.get("/env")
async def envs(user_agent: Annotated[str | None, Header()]):
    print(get_password_hash("test"))
    return {"message": settings}