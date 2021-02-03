class Blanking_Cell_Exception(Exception):
    """Exception raised when code tries to remove all values from a Cell.

    Attributes:
        cell -- Cell trying to blank
        message -- reason for exception
    """

    def __init__(self, cell_trying_to_blank, msg='You are not allowed to remove all the values from a Cell!'):
        self.cell = cell_trying_to_blank
        self.message = msg

