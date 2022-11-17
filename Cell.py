class Cell(object):

    def __init__(self, cell_address, cell_value=None):
        self.address = cell_address
        self.value = cell_value

    def __eq__(self, other):
        return isinstance(other, Cell) and self.address == other.address

    def __hash__(self):
        return hash(self.address)

    def __repr__(self):
        return f'Cell({self.address}) = {self.get_value()}'

    @property
    def get_value(self):
        return self.value

    @property
    def set_value(self, new_value):
        self.value = new_value

    def get_row(self):
        return self.address[1:]

    def get_column(self):
        return self.address[0]

    def get_row_number(self):
        return int(self.get_row())

    def get_column_number(self):
        return ord(self.get_column()) - ord('A') + 1

    def min_address_distance_to_cell(self, cell):
        row_difference = abs(self.get_row_number() - cell.get_row_number())
        column_difference = abs(self.get_column_number() - cell.get_column_number())
        return row_difference + column_difference

    def is_empty(self):
        return self.value is None
