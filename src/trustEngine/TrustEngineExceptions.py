class MissingResourceAccess(Exception):
    def __init__(self, message):
        super().__init__(message)
class UserNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)