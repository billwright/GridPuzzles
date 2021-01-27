class Cell(object):

    def __init__(self, cell_address, cell_values):
        self.address = cell_address
        self.values = cell_values

    def get_address(self):
        return self.address

    def get_values(self):
        return self.values
