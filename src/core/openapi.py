from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(self: FastAPI):
    if self.openapi_schema:
        return self.openapi_schema
    openapi_schema = get_openapi(        
        title="Customss Title",
        version="1.0.0",
        description="Custom Description",
        routes=self.routes,)
    if "securitySchemes" not in openapi_schema['components']:
        openapi_schema['components'].update({
            "securitySchemes": {
                    "CustomSecurityScheme": {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'MyCustomHeader'
                }
            }
        })
        
        for _, path in openapi_schema['paths'].items():
            for _, path_m_data in path.items():
                sec_list = [{
                    "CustomSecurityScheme": []
                }]
                if 'security' in path_m_data:
                    path_m_data['security'] += sec_list
                else:
                    path_m_data['security'] = sec_list
    # else:
    #     openapi_schema['components']['securitySchemes']['CustomSecurityScheme'] = {
    #                 'type': 'apiKey',
    #                 'in': 'header',
    #                 'name': 'MyCustomHeader'
    #             }
    #     for pkey, path in openapi_schema['paths'].items():
    #         for pm_key, path_m_data in path.items():
    #             sec_list = [{
    #                 "CustomSecurityScheme": []
    #             }]
    #             if 'security' in path_m_data:
    #                 path_m_data['security'] += sec_list
    #             else:
    #                 path_m_data['security'] = sec_list
    self.openapi_schema = openapi_schema
    return self.openapi_schema