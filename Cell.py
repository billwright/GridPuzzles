class Cell(object):

    def __init__(self, cell_address, cell_values):
        self.address = cell_address
        self.values = cell_values

    def __eq__(self, other):
        return isinstance(other, Cell) and self.address == other.address

    def __hash__(self):
        return hash(self.address)

    def __len__(self):
        return len(self.values)

    def __str__(self):
        return f'Cell({self.address}) = {self.values}'

    def remove_values(self, values_to_remove):
        for value_to_remove in values_to_remove:
            self.values = self.values.replace(value_to_remove, '')

    def get_size(self):
        return len(self.values)
