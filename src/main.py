from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from src.settings import settings
from .routers.users import router as su_router
from .routers.auth import router as auth_router
from .routers.u_examples import router as test_router

# from .routers import users

app = FastAPI()

# app.include_router(users.router)
app.include_router(su_router)
app.include_router(auth_router)
app.include_router(test_router)

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
