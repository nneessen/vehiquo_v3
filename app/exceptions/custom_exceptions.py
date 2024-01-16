class CustomException(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

#########################################################
#^################## UNIT EXCEPTIONS ####################
#########################################################

class AddUnitException(CustomException):
    pass

class DeleteUnitException(CustomException):
    pass

class UpdateUnitException(CustomException):
    pass


#########################################################
#^################## USER EXCEPTIONS ####################
#########################################################
class AddUserException(CustomException):
    pass

class DeleteUserException(CustomException):
    pass

class UpdateUserException(CustomException):
    pass

class GetUserException(CustomException):
    pass

#########################################################
#^################## STORE EXCEPTIONS ####################
#########################################################

class AddStoreException(CustomException):
    pass

class DeleteStoreException(CustomException):
    pass

class UpdateStoreException(CustomException):
    pass

class GetStoreException(CustomException):
    pass