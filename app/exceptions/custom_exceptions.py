class AddUnitException(Exception):
    def __init__(self, message, error_code):
        super().init(message)
        self.error_code = error_code



class DeleteUnitException(Exception):
    def __init__(self, message, error_code):
        super().init(message)
        self.error_code = error_code
