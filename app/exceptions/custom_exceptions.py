class CustomException(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

class AddUnitException(CustomException):
    pass

class DeleteUnitException(CustomException):
    pass

class UpdateUnitException(CustomException):
    pass