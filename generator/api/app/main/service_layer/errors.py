class DuplicateFieldError(Exception):
    def __init__(self, resource, field, value, message=""):
        super().__init__(message)
        self.resource = resource
        self.field = field
        self.value = value
