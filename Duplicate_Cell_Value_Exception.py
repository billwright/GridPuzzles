class Duplicate_Cell_Value_Exception(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)


