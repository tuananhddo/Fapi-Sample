class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

class DataNotFound(Exception):
    def __init__(self, name: str):
        self.name = name

class DuplicateData(Exception):

    def __init__(self, identity_field: str, message: str = "Data is duplicated", message_template: str = None):
        self.identity_field = identity_field
        self.message = message
        self.message_template = message_template
